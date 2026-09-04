# AI-Ready Audit — SEO, GEO & AEO Skill for Claude

**A Claude Skill that audits any website for SEO, GEO (Generative Engine Optimization), and AEO (Answer Engine Optimization) — plus a fourth, explicitly separate score most audits don't break out: Future-Readiness.** No setup step, no managed runtime, no API key, ever. Drop the folder in and it works — the entire technical layer is one ~350-line Python standard-library script.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![Claude Skill](https://img.shields.io/badge/Claude-Skill-6B4EFF)
![No API Key Required](https://img.shields.io/badge/API%20Key-Not%20Required-brightgreen)
![Zero Setup](https://img.shields.io/badge/Setup-None%20required-blue)

---

## Table of contents

- [The problem this solves](#the-problem-this-solves)
- [Read this before you install anything, including this](#read-this-before-you-install-anything-including-this)
- [Who this is for](#who-this-is-for)
- [Compared to what's already out there](#compared-to-whats-already-out-there)
- [Sample output](#sample-output)
- [Methodology — four scores, never blended](#methodology--four-scores-never-blended)
- [Quick start](#quick-start)
- [Real usage examples](#real-usage-examples)
- [How it works — no black box](#how-it-works--no-black-box)
- [FAQ](#faq)
- [Part of a small series](#part-of-a-small-series)
- [Author](#author)
- [License](#license)

---

## The problem this solves

AI crawling changed shape faster than most SEO tooling caught up. OpenAI, Anthropic, and Perplexity all now run separate training / search-index / user-fetch crawlers instead of one bot per company, and a robots.txt written against the old one-bot-per-company mental model can't even express "let AI cite me, don't let AI train on me" — a distinction real site owners increasingly want to make. Meanwhile the single most common reason a technically-fine-looking page loses to a weaker competitor is invisible from inside a browser: the page renders client-side, so a crawler that doesn't execute JavaScript sees an empty shell where the content should be. That specific failure mode — found on a real furniture-industry competitive audit that this rubric is partly built from — is often the actual headline finding, buried under a dozen smaller notes in most audits instead of leading the report.

This skill runs a technical scan (robots.txt across every current AI crawler, sitemap, llms.txt, rendering-risk detection, schema.org) using nothing but Claude's own web tools and a dependency-free script, then layers judgment on top for what a script can't measure, and reports four scores that are never collapsed into one number.

## Read this before you install anything, including this

This is one of the most crowded niches in the whole Claude Skills ecosystem right now, and it's worth saying that plainly instead of pretending otherwise. At least four separate, well-engineered, actively-maintained projects already do serious SEO/GEO/AEO work as a Claude Skill — one of them backed by a 24.8k-star, 368-skill collection with a citation tracker, per-industry E-E-A-T scoring, and automatic schema injection. If you only read one section of this README, read [Compared to what's already out there](#compared-to-whats-already-out-there) before installing anything, this tool included, and pick based on what you actually need — breadth and automation, or something small enough to read start to finish in twenty minutes.

## Who this is for

**Good fit:**
- Anyone who wants a real audit without installing a platform — clone the folder, ask a question, get a report, nothing to configure first
- A quick "why don't we show up in ChatGPT/Perplexity when we rank fine on Google" diagnostic
- Someone who wants to read the entire scoring methodology in one sitting (it's six short Markdown files) rather than trust a score they can't inspect
- A site that's never had a technical SEO pass and likely has at least one structural issue (rendering, crawler access, missing schema) worth finding before anything else

**Not a good fit — be honest about this:**
- Ongoing, continuous monitoring with historical trend tracking or a citation ledger over time — this is a point-in-time audit, several of the tools below do tracking properly
- Deep keyword research, backlink analysis, paid-search competitive intelligence, or automated content rewriting — genuinely out of scope; several tools below do this well, this one doesn't try
- An agency wanting a fully white-labeled, consultant-ready operations platform with client management built in — real use case, just not this tool's use case

## Compared to what's already out there

Named accurately, not soft-pedaled:

| Project | Scale (verified) | What it actually is | How it differs from this |
|---|---|---|---|
| [`alirezarezvani/claude-skills`](https://github.com/alirezarezvani/claude-skills) | **24.8k★ / 3.5k forks**, 364 skills incl. a dedicated `aeo` skill | The single biggest player found in this space. Its `aeo` skill alone is ~3,200 lines across 8 files: E-E-A-T + structure scoring (0–100, calibrated per industry — YMYL sites need 85+, SaaS/B2B 70, e-commerce 65), a local citation-tracking ledger across 5 LLMs with cross-LLM correlation analysis, and an optimizer that can rewrite content and inject schema.org JSON-LD directly. Part of a 24.8k-star, 18-domain mega-collection covering nearly every business function. | Their `aeo` skill optimizes and rewrites content; this toolkit only audits and hands off a to-do list, by design. Their collection requires picking through 364 skills and a plugin-marketplace install; this is one self-contained folder. No Future-Readiness-style fourth score in their model — theirs is deep on AEO specifically, this is deliberately narrower (four axes, SEO/GEO/AEO/Future-Readiness) and smaller in absolute scope. |
| [`AgriciDaniel/claude-seo`](https://github.com/AgriciDaniel/claude-seo) | **15.3k★ / 2.3k forks** | A comprehensive, actively-maintained SEO operations platform: 33 skills, 18 sub-agents, 439 passing tests, CI, security auditing, signed releases, optional paid MCP extensions (Ahrefs, Semrush, DataForSEO). Built for freelance SEO consultants scoping client engagements. Already does evidence-based reframing of the llms.txt myth. | Requires a setup step (`/seo setup` — isolated Python environment, Playwright Chromium install). This toolkit needs none of that. Trades their real breadth (local SEO, backlinks, international, e-commerce) for something legible in one sitting. |
| [`Hainrixz/claude-seo-ai`](https://github.com/Hainrixz/claude-seo-ai) | 47★ / 5 forks — small, but excellent | Two independent scores (Search SEO, AI Visibility), confidence tiers on every finding (established/directional/speculative), an opt-in fixer with real write-safety guardrails, cross-agent via Vercel Skills. Also labeled "Built for 2026-2027." | Its confidence-tier honesty is genuinely close in spirit to this toolkit's "confirmed vs. emerging" labeling — credit where due, this isn't unique framing. Structural difference: four separated scores here vs. their two; audit-only here, they have a fixer; a plain portable Skill folder here vs. their Claude Code plugin-marketplace packaging. |
| [`borghei/Claude-Skills`](https://github.com/borghei/Claude-Skills) | 368 skills, 859 tools, 20 domains | Another large general-purpose mega-collection with its own separate `marketing/aeo` skill, including a detailed citation-tracking-and-measurement methodology reference. | Same shape of tradeoff as the two collections above: enormous breadth across every business function vs. a single-purpose, small, readable tool. |
| [`SNLabat/SEO-GEO-AEO-Skill`](https://github.com/SNLabat/SEO-GEO-AEO-Skill), [`xseekio/claude-code-seo-geo-skills`](https://github.com/xseekio/claude-code-seo-geo-skills), [`199-biotechnologies/claude-skill-seo-geo-optimizer`](https://github.com/199-biotechnologies/claude-skill-seo-geo-optimizer) | smaller, listed for completeness | Cowork-only ZIP distribution; xSeek-paid-data-backed slash commands; source-file (not live-URL) optimizer, respectively. | Different distribution model, paid-data dependency, or different input (files vs. a deployed URL) in each case. |

The honest summary: if AEO is core to your work and you want automated rewriting, a citation ledger, and per-industry scoring, `alirezarezvani/claude-skills`'s `aeo` skill or `AgriciDaniel/claude-seo` are more capable choices, and they've earned their stars. This toolkit is for a narrower moment — auditing a URL in a few minutes with zero setup, four legible scores, and a methodology short enough to actually read before trusting it.

## Sample output

Illustrative output from `scripts/technical_scan.py`, showing the rendering-risk detection — the single highest-value check in the scan, and the one none of the tools above lead with as prominently:

```json
{
  "url": "https://example-furniture-store.com",
  "page": {
    "title": "Example Furniture Co.",
    "h1_count": 0,
    "schema_types_found": ["Organization"],
    "rendering_risk": {
      "level": "high",
      "visible_text_chars": 20,
      "raw_html_bytes": 4180,
      "visible_text_ratio": 0.0048,
      "script_tag_count": 4,
      "signals": [
        "SPA root marker(s) in initial HTML: root",
        "visible text is only 0.48% of raw HTML size",
        "only 20 visible chars against 4 script tags"
      ]
    }
  },
  "robots_txt": {
    "crawlers": {
      "OAI-SearchBot": { "operator": "OpenAI", "category": "search-index", "allowed_site_wide": true },
      "PerplexityBot": { "operator": "Perplexity", "category": "search-index", "allowed_site_wide": true }
    }
  },
  "llms_txt": { "present": false }
}
```

A crawler that can't run JavaScript sees 20 characters of content on this homepage regardless of how good the content is once rendered in a browser. This is the finding that should lead the report.

## Methodology — four scores, never blended

| Score | What it measures |
|---|---|
| **SEO** | Crawlability, rendering risk, sitemap, heading structure, meta tags |
| **GEO** | Whether AI search/citation crawlers can reach you, `llms.txt`, structured data, third-party citation footprint |
| **AEO** | Whether content leads with real answers, has E-E-A-T signals, is written to be quoted |
| **Future-Readiness** | Crawler-tier granularity, agent-fetchable structure, structured-data depth, freshness signals — explicitly labeled confirmed-current vs. emerging-pattern, never blurred together |

Every threshold traces to a cited source in `references/citation-research-notes.md` — including the honest parts: schema markup's measured AI-citation lift is modest (~2.4% in one large test), most published `llms.txt` files get zero fetch requests, and Google retired FAQ rich results for all sites as of May 7, 2026.

## Quick start

**Claude Code / Cowork:**
```bash
git clone https://github.com/Jannat63/AI-Ready-Audit-SEO-GEO-AEO-Skill-for-Claude.git ai-ready-audit
# point your Claude Code / Cowork skills directory at this folder,
# or copy it into ~/.claude/skills/ai-ready-audit
```

**claude.ai (with code execution enabled):** upload this folder or its ZIP into a conversation and ask about auditing a URL — Claude finds and uses the skill automatically.

No install script, no `setup` command, no browser binary to download, no plugin marketplace. Deliberate scope choice — see the comparison above.

## Real usage examples

> *"Audit example.com for SEO, GEO, and AEO — is it AI-ready?"*

> *"Why does our competitor outrank us in ChatGPT and Google, and we don't show up at all?"*

> *"Is my site's robots.txt blocking AI crawlers by accident?"*

> *"Give me a Quick Audit of this URL, I just want the top 3 issues."*

## How it works — no black box

```
ai-ready-audit/
├── SKILL.md
├── scripts/technical_scan.py         # stdlib-only, zero pip installs
├── references/
│   ├── scoring-rubric.md
│   ├── ai-crawler-directory.md
│   ├── llms-txt-guide.md
│   ├── future-readiness-signals.md
│   └── citation-research-notes.md
└── assets/report-template.md
```

Total footprint: one script, five reference files, one template — open any of them directly.

## FAQ

**Is this actually the best SEO/GEO/AEO Claude Skill?**
No, and this README says so directly — `alirezarezvani/claude-skills` and `AgriciDaniel/claude-seo` are both larger, more capable, more battle-tested projects for anyone who wants breadth or automated fixes. This is a smaller, narrower, zero-setup tool. Pick based on what's in the comparison table above.

**Does it need an API key?**
No, never, at any tier. Several of the tools above also offer a genuinely free base tier now, to be fair — the difference is there's no paid tier to begin with here.

**Why does a fourth-score, zero-setup audit tool matter if bigger tools already do AEO well?**
Because "bigger and more capable" and "fast to install and easy to fully verify" are different products serving different moments — sometimes the second one is what's actually needed.

**Can this fix issues automatically?**
No, by design — it hands off a prioritized, owner-split action table rather than writing changes itself. `Hainrixz/claude-seo-ai` and `alirezarezvani/claude-skills`'s `aeo` skill both do automated changes if that's what's wanted.

## Part of a small series

This is skill 1 of a small set of practitioner-built Claude Skills — [`sheet-cms-toolkit`](https://github.com/Jannat63/Sheet-as-CMS-Toolkit-A-Claude-Skill-for-Google-Sheets-Backed-Sites) is skill 2, a validator for Google-Sheets-backed sites with no direct competitor found even after checking against five separate 300+-skill collections, and [`motion-audit-toolkit`](https://github.com/Jannat63/Motion-Audit-Toolkit---A-Claude-Skill-for-Auditing-Shipped-Animations) is skill 3, auditing shipped animations for performance, accessibility, and consistency.

## Author

Built by **Ahsan Jannat** — SEO, AEO & GEO specialist and Meta Ads consultant. More work at [ahsan-jannat.netlify.app](https://ahsan-jannat.netlify.app).

## License

MIT — see [LICENSE](./LICENSE).

## Keywords

Claude Skill, SEO audit, GEO audit, AEO audit, Generative Engine Optimization, Answer Engine Optimization, AI search visibility, AI crawler robots.txt, llms.txt, ChatGPT citations, Claude citations, Perplexity citations, AI-ready website, Claude Code skill, rendering risk audit, client-side rendering SEO
