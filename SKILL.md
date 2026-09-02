---
name: ai-ready-audit
description: Runs a full SEO, GEO (Generative Engine Optimization), and AEO (Answer Engine Optimization) audit on any website using only Claude's own web search and fetch tools — no paid API keys, no DataForSEO/Ahrefs/SE Ranking/xSeek subscription required. Scores four dimensions: traditional SEO, AI-citation readiness (GEO), direct-answer readiness (AEO), and Future-Readiness (whether the site is built for where AI crawling and agent browsing are heading, not just today's checklist). Use this skill whenever the user asks to audit a website or page for SEO, mentions GEO, AEO, "AI search", "AI visibility", ChatGPT/Claude/Perplexity citations, llms.txt, AI crawlers, robots.txt for AI bots, or asks why a competitor outranks them in Google or gets cited by AI and they don't. Also trigger when the user pastes a URL and asks how "AI-ready", "AI-friendly", or "future-proof" it is, or wants a side-by-side SEO/GEO comparison against a competitor's site.
compatibility: Requires WebFetch/web_search-equivalent tools and a code execution environment that can run Python 3 (standard library only — no pip installs needed). Works in Claude Code, Cowork, and claude.ai with code execution enabled.
---

# AI-Ready Audit

A practitioner-built SEO/GEO/AEO audit skill. It exists because most audit skills either (a) require a paid third-party API key before they'll do anything, or (b) grade a site against today's checklist and go stale the day crawler behavior shifts. This skill does neither: it uses only the tools Claude already has, and it scores a fourth dimension — **Future-Readiness** — that most competing skills skip entirely.

## Why a fourth score

SEO, GEO, and AEO all describe *is this site working right now*. But AI crawling is moving fast: crawlers have split into training/search/user-fetch variants in the last year, IDE agents (Claude Code, Cursor, Windsurf) now fetch `llms.txt` directly when working with a codebase, and early agent-to-agent content exchange patterns are emerging. A site that only passes today's checklist can still be badly positioned for where this goes next. Future-Readiness checks for that: crawler-tier granularity in robots.txt, agent-fetchable content structure, structured-data depth beyond the minimum, and freshness signals — not speculation, just the parts of "AI-ready" that current audits don't measure.

Be honest about uncertainty here. Some of what Future-Readiness checks for (e.g., agent-to-agent commerce, richer llms.txt adoption) is an emerging pattern, not a settled ranking factor — the report should say so plainly rather than present it as guaranteed impact.

## Workflow

### Step 1 — Ask one question, every time

Before doing anything else, ask the user:

> **Quick Audit** (2–3 min, homepage + robots.txt/sitemap/llms.txt, top-line scores) or **Full Audit** (10–15 min, crawls 5–8 key pages — home, about, services/products, blog, FAQ/contact — full scored report with prioritized action tables)?

Don't skip this even if the request sounds like it obviously wants a full audit — a quick gut-check is often what's actually wanted, and asking takes one turn.

### Step 2 — Run the technical scan

Run `scripts/technical_scan.py` against the target URL. It needs nothing but Python's standard library — no `pip install` step, which is part of the point.

```bash
python3 scripts/technical_scan.py https://example.com
```

This returns JSON covering, per URL scanned:
- `robots_txt`: parsed rules for every known AI crawler (see `references/ai-crawler-directory.md`), split into training / search-index / user-fetch categories, plus whether each is allowed or blocked
- `sitemap`: presence, URL count, lastmod range
- `llms_txt`: presence, and whether it follows the spec (single H1, blockquote summary, curated link sections) — see `references/llms-txt-guide.md`
- `rendering_risk`: a heuristic score for whether the page's real content lives in the initial HTML or only appears after JavaScript executes. This check exists because client-side-only rendering is one of the most common — and most invisible to the site owner — reasons a page loses to a technically weaker competitor for a target keyword. If a crawler fetches an empty shell, nothing else on this list matters.
- `schema`: every JSON-LD block found, with `@type` values
- `headings`: heading tag structure and whether there's exactly one H1
- `meta`: title, meta description, canonical tag

For a Full Audit, run this once per page (home, about, services, blog, FAQ/contact — whichever exist). Skip any page that 404s or redirects somewhere unexpected, and note that in the report.

If the script errors on a URL (site blocks bots, times out, returns non-200), don't silently drop it — tell the user which page failed and why, and continue with what did work.

### Step 3 — Layer in what the script can't measure

The script gives deterministic technical facts. It cannot judge content quality, so after it runs, read the fetched pages yourself (WebFetch or equivalent) and assess:

- **Answer-first structure** (AEO): does each key page lead with a direct, quotable answer to the question a visitor or AI system would be asking, before the elaboration? Vague marketing copy up top is a real AEO cost.
- **E-E-A-T signals**: named authors with credentials, cited sources, visible freshness/last-updated dates, physical/business legitimacy signals (address, real contact info, About page depth).
- **Third-party citation footprint** (GEO): use web_search for `"<brand name>" reddit`, `"<brand name>" review`, and `site:<competitor-heavy platform>` queries relevant to the industry. Sites with an active footprint on platforms AI systems cite heavily (Reddit, LinkedIn, Wikipedia, G2/Capterra-equivalents for the industry) are meaningfully more likely to get cited — this is measurable, not a guess, and worth 2–3 targeted searches rather than skipping it.
- **Competitive angle** (if a competitor URL was given): run the same scan on both, and lead the report with the *specific, verifiable* gap — not a generic list. If one site renders client-side and the other doesn't, that's usually the headline finding, not buried on page 3.

### Step 4 — Score and report

Read `references/scoring-rubric.md` for the exact scoring method before assigning numbers — don't eyeball the 1–10 scores. Each of the four dimensions (SEO / GEO / AEO / Future-Readiness) gets a score with the specific evidence behind it, not just a number.

Build the report using the structure in `assets/report-template.md`. Every audit produces:

1. A short in-chat summary: the four scores, the single biggest strength, and the top 3 priorities named specifically (not "improve SEO" — "your homepage's product grid is client-side rendered; a crawler sees an empty `<div id='root'>`").
2. A full report as a downloadable document (use the docx or pdf skill if available in this environment) with: executive summary, signal-by-signal findings per dimension, a prioritized action table split by owner (**Developer actions** vs. **Content/SEO actions** — most real fixes need both, and separating them is what actually gets things shipped), and a "what's already working" section. Audits that only list problems get ignored; naming genuine strengths makes the priorities more credible.

Don't inflate scores to be encouraging, and don't manufacture urgency to make the findings feel more valuable than they are. If a site is already in good shape, say so plainly — a short report with real findings beats a padded one.

## Reference files

- `references/scoring-rubric.md` — exact scoring method for all four dimensions, with the evidence behind each threshold
- `references/ai-crawler-directory.md` — every current AI crawler user-agent, which company runs it, and whether it's training/search/user-fetch
- `references/llms-txt-guide.md` — the llms.txt spec, a good example, and an honest note on how unproven its actual impact still is
- `references/future-readiness-signals.md` — what the fourth score checks for and why, including what's confirmed vs. emerging
- `references/citation-research-notes.md` — the primary research this rubric is grounded in, with sources, so scores are defensible if someone asks "says who?"
