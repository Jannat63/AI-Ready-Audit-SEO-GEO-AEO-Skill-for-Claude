#!/usr/bin/env python3
"""
technical_scan.py — deterministic technical scan for the ai-ready-audit skill.

Standard library only. No pip installs, no API keys, no paid SEO tool
subscription. This is the whole point of the skill: everything it needs,
Claude already has.

Usage:
    python3 technical_scan.py https://example.com [https://example.com/about ...]

Prints JSON to stdout: one result object per URL, covering robots.txt
(with a breakdown of every known AI crawler), sitemap.xml, llms.txt, and a
per-page structural scan (headings, schema.org JSON-LD, meta tags, and a
rendering-risk heuristic for client-side-only pages).

This script produces facts, not scores. Scoring happens in the skill
workflow using references/scoring-rubric.md — keep judgment calls out of
this file so the output stays reproducible.
"""

import sys
import json
import re
import time
import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

USER_AGENT = "AIReadyAuditBot/1.0 (+https://github.com/ahsan-jannat/ai-ready-audit)"
TIMEOUT = 12

# name -> (operator, category). category is one of:
#   training     -> feeds model training, no immediate citation impact
#   search-index -> populates the index an AI answer is assembled from
#   user-fetch   -> live fetch triggered by a real user's question
AI_CRAWLERS = {
    "GPTBot": ("OpenAI", "training"),
    "OAI-SearchBot": ("OpenAI", "search-index"),
    "ChatGPT-User": ("OpenAI", "user-fetch"),
    "ClaudeBot": ("Anthropic", "training"),
    "Claude-SearchBot": ("Anthropic", "search-index"),
    "Claude-User": ("Anthropic", "user-fetch"),
    "PerplexityBot": ("Perplexity", "search-index"),
    "Perplexity-User": ("Perplexity", "user-fetch"),
    "Google-Extended": ("Google", "training"),
    "Googlebot": ("Google", "search-index"),
    "Applebot-Extended": ("Apple", "training"),
    "Amazonbot": ("Amazon", "training"),
    "meta-externalagent": ("Meta", "training"),
    "Bytespider": ("ByteDance", "training"),
    "CCBot": ("Common Crawl", "training"),
    "Diffbot": ("Diffbot", "training"),
}


def fetch(url, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {
                "ok": True,
                "status": resp.status,
                "body": resp.read(),
                "content_type": resp.headers.get("Content-Type", ""),
                "final_url": resp.geturl(),
            }
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": str(e)}
    except Exception as e:
        return {"ok": False, "status": None, "error": str(e)}


def parse_robots(base_url):
    robots_url = urllib.parse.urljoin(base_url, "/robots.txt")
    res = fetch(robots_url)
    result = {"present": False, "url": robots_url, "crawlers": {}, "sitemap_hint": None}
    if not res["ok"]:
        return result
    result["present"] = True
    text = res["body"].decode("utf-8", errors="replace")

    current_agents = []
    rules = {}
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            current_agents = []
            continue
        if ":" not in line:
            continue
        field, _, value = line.partition(":")
        field = field.strip().lower()
        value = value.strip()
        if field == "user-agent":
            current_agents.append(value)
            rules.setdefault(value, [])
        elif field in ("disallow", "allow") and current_agents:
            for agent in current_agents:
                rules.setdefault(agent, []).append((field, value))
        elif field == "sitemap":
            result["sitemap_hint"] = value

    def agent_allowed(agent_rules):
        # Whole-site allow/disallow only. Path-scoped rules exist in the
        # file but this heuristic doesn't resolve precedence for them —
        # flag path-scoped rules for manual review instead of guessing.
        blocked = False
        has_path_scoped_rule = False
        for directive, path in agent_rules:
            if path in ("/", ""):
                if directive == "disallow" and path == "/":
                    blocked = True
                elif directive == "allow" or (directive == "disallow" and path == ""):
                    blocked = False
            else:
                has_path_scoped_rule = True
        return (not blocked), has_path_scoped_rule

    wildcard_rules = rules.get("*", [])
    for bot_name, (operator, category) in AI_CRAWLERS.items():
        matched_key = next((k for k in rules if k.lower() == bot_name.lower()), None)
        agent_rules = rules.get(matched_key, []) if matched_key else wildcard_rules
        allowed, has_path_rules = agent_allowed(agent_rules)
        result["crawlers"][bot_name] = {
            "operator": operator,
            "category": category,
            "explicitly_listed": matched_key is not None,
            "allowed_site_wide": allowed,
            "has_path_scoped_rules_to_review": has_path_rules,
        }
    return result


def check_sitemap(base_url, robots_hint):
    candidates = [c for c in [robots_hint, urllib.parse.urljoin(base_url, "/sitemap.xml")] if c]
    for url in candidates:
        res = fetch(url)
        if res["ok"] and res["status"] == 200:
            try:
                root = ET.fromstring(res["body"])
                ns = root.tag.split("}")[0] + "}" if root.tag.startswith("{") else ""
                locs = root.findall(f".//{ns}loc")
                lastmods = root.findall(f".//{ns}lastmod")
                return {
                    "present": True,
                    "url": url,
                    "url_count": len(locs),
                    "is_index": root.tag.endswith("sitemapindex"),
                    "lastmod_sample": [el.text for el in lastmods[:5]],
                }
            except ET.ParseError:
                return {"present": True, "url": url, "url_count": None, "note": "found but not valid XML"}
    return {"present": False, "url": candidates[-1] if candidates else None}


def check_llms_txt(base_url):
    url = urllib.parse.urljoin(base_url, "/llms.txt")
    res = fetch(url)
    if not res["ok"] or res["status"] != 200:
        return {"present": False, "url": url}
    text = res["body"].decode("utf-8", errors="replace")
    lines = [l for l in text.splitlines() if l.strip()]
    has_h1 = any(l.strip().startswith("# ") for l in lines[:5])
    has_blockquote = any(l.strip().startswith(">") for l in lines[:8])
    return {
        "present": True,
        "url": url,
        "spec_compliant_shape": has_h1 and has_blockquote,
        "has_h1": has_h1,
        "has_blockquote_summary": has_blockquote,
        "section_count": sum(1 for l in lines if l.strip().startswith("## ")),
        "link_count": len(re.findall(r"\[.+?\]\(https?://[^\s)]+\)", text)),
    }


class PageParser(HTMLParser):
    """Lightweight structural parser. Stdlib only, on purpose."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self.meta_description = None
        self.canonical = None
        self.headings = []
        self.script_tags = 0
        self.jsonld_blocks = []
        self.visible_text_chars = 0
        self.spa_root_markers = []
        self._in_title = False
        self._in_script = False
        self._script_is_jsonld = False
        self._current_script_buffer = []
        self._in_heading = None
        self._heading_buffer = []
        self._current_skip_tag = None
        self._skip_text_tags = {"script", "style", "noscript"}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "meta" and (a.get("name") or "").lower() == "description":
            self.meta_description = a.get("content")
        if tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.canonical = a.get("href")
        if tag == "script":
            self.script_tags += 1
            self._in_script = True
            self._script_is_jsonld = (a.get("type") or "").lower() == "application/ld+json"
            self._current_script_buffer = []
        if tag in self._skip_text_tags:
            self._current_skip_tag = tag
        if tag in ("h1", "h2", "h3", "h4"):
            self._in_heading = tag
            self._heading_buffer = []
        if tag == "div" and (a.get("id") or "").lower() in ("root", "__next", "app", "___gatsby"):
            self.spa_root_markers.append(a.get("id").lower())

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script":
            content = "".join(self._current_script_buffer)
            if self._script_is_jsonld and content.strip():
                self.jsonld_blocks.append(content.strip())
            self._in_script = False
        if tag in self._skip_text_tags and self._current_skip_tag == tag:
            self._current_skip_tag = None
        if self._in_heading == tag:
            self.headings.append((tag, "".join(self._heading_buffer).strip()))
            self._in_heading = None

    def handle_data(self, data):
        if self._in_title and self.title is None:
            self.title = data.strip()
        if self._in_script:
            self._current_script_buffer.append(data)
            return
        if self._current_skip_tag:
            return
        if self._in_heading:
            self._heading_buffer.append(data)
        if data.strip():
            self.visible_text_chars += len(data.strip())


def analyze_page(url):
    res = fetch(url)
    if not res["ok"]:
        return {"ok": False, "status": res.get("status"), "error": res.get("error")}
    html = res["body"].decode("utf-8", errors="replace")
    parser = PageParser()
    try:
        parser.feed(html)
    except Exception as e:
        return {"ok": False, "error": f"parse error: {e}"}

    raw_len = len(html)
    visible_ratio = round(parser.visible_text_chars / raw_len, 4) if raw_len else 0

    # Rendering-risk heuristic: a *signal to verify*, not a verdict.
    signals = []
    if parser.spa_root_markers:
        signals.append(f"SPA root marker(s) in initial HTML: {', '.join(set(parser.spa_root_markers))}")
    if visible_ratio < 0.02:
        signals.append(f"visible text is only {visible_ratio*100:.2f}% of raw HTML size")
    if parser.visible_text_chars < 200 and parser.script_tags >= 3:
        signals.append(f"only {parser.visible_text_chars} visible chars against {parser.script_tags} script tags")
    risk_level = "high" if len(signals) >= 2 else ("medium" if signals else "low")

    jsonld_types = []
    for block in parser.jsonld_blocks:
        try:
            data = json.loads(block)
            for item in (data if isinstance(data, list) else [data]):
                if isinstance(item, dict) and "@type" in item:
                    t = item["@type"]
                    jsonld_types.extend(t if isinstance(t, list) else [t])
        except (json.JSONDecodeError, TypeError):
            jsonld_types.append("(unparseable JSON-LD block — verify manually)")

    return {
        "ok": True,
        "final_url": res.get("final_url", url),
        "status": res["status"],
        "title": parser.title,
        "meta_description": parser.meta_description,
        "canonical": parser.canonical,
        "headings": [{"level": lvl, "text": txt} for lvl, txt in parser.headings if txt],
        "h1_count": sum(1 for lvl, _ in parser.headings if lvl == "h1"),
        "schema_types_found": jsonld_types,
        "rendering_risk": {
            "level": risk_level,
            "visible_text_chars": parser.visible_text_chars,
            "raw_html_bytes": raw_len,
            "visible_text_ratio": visible_ratio,
            "script_tag_count": parser.script_tags,
            "signals": signals,
        },
    }


def scan_url(url, robots_cache):
    parsed = urllib.parse.urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    if base_url not in robots_cache:
        robots = parse_robots(base_url)
        robots_cache[base_url] = {
            "robots": robots,
            "sitemap": check_sitemap(base_url, robots.get("sitemap_hint")),
            "llms_txt": check_llms_txt(base_url),
        }
    domain_data = robots_cache[base_url]
    return {
        "url": url,
        "robots_txt": domain_data["robots"],
        "sitemap": domain_data["sitemap"],
        "llms_txt": domain_data["llms_txt"],
        "page": analyze_page(url),
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: technical_scan.py <url> [<url> ...]"}))
        sys.exit(1)
    robots_cache = {}
    results = []
    for u in sys.argv[1:]:
        results.append(scan_url(u, robots_cache))
        time.sleep(0.5)  # be a polite crawler
    output = {
        "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "notes": (
            "robots_txt.allowed_site_wide only resolves whole-site Allow:/ vs "
            "Disallow:/ — pages flagged has_path_scoped_rules_to_review need a "
            "manual look. rendering_risk is a heuristic (visible-text ratio + "
            "SPA markers), not a certainty — spot-check with view-source when "
            "risk_level is medium or high."
        ),
        "results": results,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
