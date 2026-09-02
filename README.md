# AI-Ready Audit — SEO, GEO & AEO Skill for Claude

**A Claude Skill that audits any website for SEO, GEO (Generative Engine Optimization), and AEO (Answer Engine Optimization) — plus a fourth score most audits skip: Future-Readiness, whether the site is built for where AI crawling is headed, not just where it is today.**

No API key. No DataForSEO, Ahrefs, or SE Ranking subscription. No `xseek`/paid CLI. It runs on Claude's own web search and fetch tools plus one dependency-free Python script — install it and it works.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![Claude Skill](https://img.shields.io/badge/Claude-Skill-6B4EFF)
![No API Key Required](https://img.shields.io/badge/API%20Key-Not%20Required-brightgreen)

---

## Why this exists

Open almost any SEO/GEO/AEO skill on GitHub right now and one of two things is true: it needs a paid API key before it'll run an audit, or it's grading your site against a checklist that was accurate the day it was written and is already a step behind. AI crawling didn't sit still this year — OpenAI, Anthropic, and Perplexity all split their crawlers into training / search-index / user-fetch categories, coding agents started reading `llms.txt` directly, and most audit tools haven't caught up to any of that.

**AI-Ready Audit** is built by a working SEO/AEO/GEO practitioner, not a tool vendor, on one rule: everything it checks has to be either a verifiable technical fact or clearly labeled as an emerging pattern — never blurred together to sound more urgent than it is.

## What it checks

| Score | What it measures |
|---|---|
| **SEO** | Crawlability, rendering risk (is your content actually in the HTML a bot sees, or only after JavaScript runs?), sitemap, heading structure, meta tags |
| **GEO** | Whether AI search/citation crawlers can actually reach you, `llms.txt`, structured data, and your third-party citation footprint |
| **AEO** | Whether your content leads with real answers, has E-E-A-T signals, and is written to be quoted |
| **Future-Readiness** | Crawler-tier granularity, agent-fetchable content structure, structured-data depth, freshness signals — confirmed current AI-agent behavior that today's SEO/GEO checklists don't measure yet |

Every score comes with the specific evidence behind it — not "improve your SEO," but "your homepage renders inside `<div id='root'>` with 40 characters of visible text against 12 script tags; a crawler that doesn't execute JavaScript sees almost nothing."

## Quick start

**Claude Code / Cowork:**
```bash
git clone https://github.com/<your-username>/ai-ready-audit.git
# then point your Claude Code / Cowork skills directory at this folder,
# or copy it into ~/.claude/skills/ai-ready-audit
```

**claude.ai (with code execution enabled):** upload this folder or its ZIP into a conversation and ask Claude to audit a URL — it will find and use the skill automatically.

Then just ask, in plain language:

> *"Audit hatil.com for SEO, GEO, and AEO — is it AI-ready?"*
> *"Why does [competitor] outrank us in ChatGPT and Google, and we don't show up at all?"*
> *"Is my site's robots.txt blocking AI crawlers by accident?"*

The skill asks one question first — Quick Audit or Full Audit — then runs.

## What you get

A same-chat summary with all four scores and the top 3 priorities, plus a full downloadable report: executive summary, evidence for every score, a "what's already working" section, and a priority action table **split by owner** — Developer actions and Content/SEO actions — because most real fixes need both, and most audits hand you one undifferentiated list nobody actually assigns.

## How it works — no black box

```
ai-ready-audit/
├── SKILL.md                          # the workflow Claude follows
├── scripts/
│   └── technical_scan.py             # stdlib-only Python: robots.txt, sitemap,
│                                      # llms.txt, rendering-risk, schema.org — zero pip installs
├── references/
│   ├── scoring-rubric.md             # exact point-by-point scoring method
│   ├── ai-crawler-directory.md       # every current AI bot, by category
│   ├── llms-txt-guide.md             # the spec + an honest adoption reality check
│   ├── future-readiness-signals.md   # confirmed vs. emerging, kept separate on purpose
│   └── citation-research-notes.md    # the primary research the rubric is grounded in
└── assets/
    └── report-template.md            # the exact report structure
```

Every scoring threshold is traceable to a reason in `references/`. If a finding in your report seems off, the rubric that produced it is sitting right there in plain Markdown — nothing about the methodology is hidden behind an API response you can't inspect.

## What makes this different

- **Zero paid dependencies.** No API key, ever. The technical scan is pure Python standard library.
- **Evidence-cited, not vibes-based.** The scoring rubric is built on primary research (cited in `citation-research-notes.md`), including an honest accounting of what actually moves the needle — e.g., schema markup's real measured impact is modest, and the rubric says so instead of overselling it.
- **Future-Readiness as its own score**, clearly separating what's confirmed current AI-agent behavior from what's an emerging, unproven pattern — most competing audits don't measure this dimension at all.
- **Built and used by a practitioner**, not written as a portfolio piece for a tool vendor.

## Roadmap

This is the first of a small set of practitioner-built Claude Skills — more coming. Star the repo to catch the next ones.

## Author

Built by **Ahsan Jannat** — SEO, AEO & GEO specialist and Meta Ads consultant. More work at [ahsan-jannat.netlify.app](https://ahsan-jannat.netlify.app).

## License

MIT — see [LICENSE](./LICENSE). Use it, fork it, improve it.

## Keywords

Claude Skill, SEO audit, GEO audit, AEO audit, Generative Engine Optimization, Answer Engine Optimization, AI search visibility, AI crawler robots.txt, llms.txt, ChatGPT citations, Claude citations, Perplexity citations, AI-ready website, Claude Code skill, Claude Cowork skill
