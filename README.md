# AI-Ready Audit — SEO, GEO & AEO Skill for Claude

**A Claude Skill that audits any website for SEO, GEO (Generative Engine Optimization), and AEO (Answer Engine Optimization) — plus a fourth, explicitly separate score most audits don't break out: Future-Readiness.** No setup step, no managed runtime, no API key, ever. Drop the folder in and it works — the entire technical layer is one ~350-line Python standard-library script.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![Claude Skill](https://img.shields.io/badge/Claude-Skill-6B4EFF)
![No API Key Required](https://img.shields.io/badge/API%20Key-Not%20Required-brightgreen)
![Zero Setup](https://img.shields.io/badge/Setup-None%20required-blue)

---

## Table of contents

- [The problem this solves](#the-problem-this-solves)
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

This skill runs a technical scan (robots.txt across every current AI crawler, sitemap, llms.txt, rendering-risk detection, schema.org) using nothing but Claude's own web tools and a dependency-free script, then layers judgment on top for what a script can't measure — answer-first structure, E-E-A-T signals, third-party citation footprint — and reports four scores that are never collapsed into one number, because a site can be strong on one and weak on another and that's the useful information.

## Who this is for

**Good fit:**
- Anyone who wants a real audit without installing a platform — clone the folder, ask a question, get a report
- A quick "why don't we show up in ChatGPT/Perplexity when we rank fine on Google" diagnostic
- Someone who wants to read the entire scoring methodology in one sitting (it's six short Markdown files) rather than trust a black-box score
- A site that's never had a technical SEO pass and likely has at least one structural issue (rendering, crawler access, missing schema) worth finding before anything else

**Not a good fit — be honest about this:**
- Ongoing, continuous monitoring with historical trend tracking — this is a point-in-time audit tool, not a dashboard
- Deep keyword research, backlink analysis, or paid-search competitive intelligence — genuinely out of scope, and any tool claiming to do all of this *and* be simple is probably not being straight with you about the tradeoff
- An agency wanting a fully white-labeled, consultant-ready operations platform with client management built in — see the comparison below, that's a real use case, just not this tool's use case

## Compared to what's already out there

This space is more mature than a first search suggests, and it's worth naming the real competitors accurately rather than pretending the field is empty.

| Project | Stars (verified) | What it actually is | How it differs from this |
|---|---|---|---|
| [`AgriciDaniel/claude-seo`](https://github.com/AgriciDaniel/claude-seo) | ~15.3k★ / 2.3k forks | A genuinely comprehensive, actively-maintained SEO operations platform: 33 skills, 18 sub-agents, 380 files, 439 passing tests, CI, security auditing (SSRF protection, secret scanning, `pip-audit`), signed releases, optional paid MCP extensions (Ahrefs, Semrush, DataForSEO). Explicitly built for freelance SEO consultants scoping client engagements. It already does evidence-based reframing of the llms.txt myth — this isn't unique to this toolkit, and it's a good sign when a big incumbent does it too. | Requires a setup step (`/seo setup` — creates an isolated Python environment and installs Playwright Chromium). This toolkit needs none of that: no managed runtime, no browser install, one script. Trade real breadth (25+ SEO sub-domains: local SEO, backlinks, international, e-commerce) for something you can read start to finish and understand every scoring decision in about 20 minutes. Different tool for a different moment — theirs for running an SEO practice, this for a fast, transparent, no-install audit. |
| [`Hainrixz/claude-seo-ai`](https://github.com/Hainrixz/claude-seo-ai) | 47★ / 5 forks | Small but excellent — worth knowing about even at low star count. Two independent scores (Search SEO, AI Visibility), never blended. Every finding carries a confidence tier (established / directional / speculative). An opt-in fixer with real write-safety guardrails (dry-run by default, git-aware, refuses a dirty tree, never touches `.git`/secrets/lockfiles). Cross-agent via Vercel Skills (Cursor, Codex, Gemini CLI, Windsurf), not just Claude Code. Also explicitly labeled "Built for 2026-2027." | The confidence-tier honesty philosophy is genuinely close to what this toolkit does with "confirmed vs. emerging" — credit where due. The structural difference: four explicitly separated scores here (SEO / GEO / AEO / Future-Readiness) vs. their two; this toolkit is audit-only with no fixer at all, by design, handing off to a Developer/Content action table instead of writing changes itself; and this is a single portable Skill folder rather than a Claude Code plugin-marketplace install with slash commands. |
| [`SNLabat/SEO-GEO-AEO-Skill`](https://github.com/SNLabat/SEO-GEO-AEO-Skill) | — | ZIP-distributed specifically for Claude's Cowork desktop app; outputs Word/PDF reports. | Narrower distribution model (Cowork-only ZIP vs. a portable skill folder that works anywhere Skills are supported). |
| [`xseekio/claude-code-seo-geo-skills`](https://github.com/xseekio/claude-code-seo-geo-skills) | — | Six slash commands backed by xSeek's own tracked search data — genuinely useful if already paying for that service. | Requires the underlying paid data service to be meaningful; this toolkit has no paid dependency at any tier. |
| [`199-biotechnologies/claude-skill-seo-geo-optimizer`](https://github.com/199-biotechnologies/claude-skill-seo-geo-optimizer) | — | Analyzes HTML/Markdown/React source files directly for SEO/GEO signals — a content-file optimizer. | Different input entirely: this toolkit audits a *live, deployed* URL (what a crawler actually sees), not source files before they ship. |

The honest summary: if you want a full SEO consultancy operating system, `claude-seo` is the more capable choice and it's earned its stars. If you want something that audits a URL in a few minutes with zero setup, four legible scores, and a methodology you can actually read and verify, that's what this is for.

## Sample output

Illustrative output from `scripts/technical_scan.py`, showing the rendering-risk detection that's the single highest-value check in the whole scan — this is the exact pattern from the real-world finding this toolkit is partly built around, where a competitor's client-side-rendered homepage was effectively invisible to non-JS crawlers while a technically weaker page outranked it:

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

A crawler that can't run JavaScript sees 20 characters of content on this homepage — the title and nothing else — regardless of how good the actual content is once rendered in a browser. This is the finding that should lead the report, not get buried on page three.

## Methodology — four scores, never blended

| Score | What it measures |
|---|---|
| **SEO** | Crawlability, rendering risk, sitemap, heading structure, meta tags |
| **GEO** | Whether AI search/citation crawlers can reach you, `llms.txt`, structured data, third-party citation footprint |
| **AEO** | Whether content leads with real answers, has E-E-A-T signals, is written to be quoted |
| **Future-Readiness** | Crawler-tier granularity, agent-fetchable structure, structured-data depth, freshness signals — explicitly labeled confirmed-current vs. emerging-pattern, never blurred together |

Every threshold in the scoring rubric traces to a cited source in `references/citation-research-notes.md` — including the honest parts: schema markup's measured AI-citation lift is modest (~2.4% in one large test), most published `llms.txt` files get zero fetch requests, and Google retired FAQ rich results for all sites as of May 7, 2026. The rubric says all of this plainly instead of overselling any single lever.

## Quick start

**Claude Code / Cowork:**
```bash
git clone https://github.com/<your-username>/ai-ready-audit.git
# point your Claude Code / Cowork skills directory at this folder,
# or copy it into ~/.claude/skills/ai-ready-audit
```

**claude.ai (with code execution enabled):** upload this folder or its ZIP into a conversation and ask about auditing a URL — Claude finds and uses the skill automatically.

No install script, no `setup` command, no browser binary to download. That's a deliberate scope choice, not an oversight — see [Compared to what's already out there](#compared-to-whats-already-out-there).

## Real usage examples

> *"Audit example.com for SEO, GEO, and AEO — is it AI-ready?"*

> *"Why does our competitor outrank us in ChatGPT and Google, and we don't show up at all?"*

> *"Is my site's robots.txt blocking AI crawlers by accident?"*

> *"Give me a Quick Audit of this URL, I just want the top 3 issues."*

> *"Run a Full Audit and give me separate action tables for my developer and my content writer."*

## How it works — no black box

```
ai-ready-audit/
├── SKILL.md                          # the workflow Claude follows
├── scripts/
│   └── technical_scan.py             # stdlib-only Python: robots.txt (every current
│                                      # AI crawler, categorized), sitemap, llms.txt,
│                                      # rendering-risk, schema.org — zero pip installs
├── references/
│   ├── scoring-rubric.md             # exact point-by-point scoring method
│   ├── ai-crawler-directory.md       # every current AI bot, by category
│   ├── llms-txt-guide.md             # the spec + an honest adoption reality check
│   ├── future-readiness-signals.md   # confirmed vs. emerging, kept explicitly separate
│   └── citation-research-notes.md    # the primary research the rubric is grounded in
└── assets/
    └── report-template.md            # the exact report structure
```

Total footprint: one script, five reference files, one template. Open any of them directly — nothing about the scoring logic sits behind an API call you can't inspect.

## FAQ

**Is this better than `claude-seo` (15k★)?**
No, not across the board, and see [above](#compared-to-whats-already-out-there) for the honest comparison — it's a more capable tool for running an SEO practice. This is a different, smaller thing: a transparent, zero-setup audit you can verify by reading five files.

**Does it need a Google PageSpeed / Ahrefs / DataForSEO API key?**
No, never, at any tier. That's true of every tool in the comparison table too, to be fair — most now offer a genuinely free base tier. The difference here is there's no optional paid tier to begin with, because there's nothing more the tool does if you added one.

**Will the scores match what a paid tool like Ahrefs or Semrush would show?**
Not directly comparable — this measures AI-crawler and citation readiness specifically, which most classic SEO tools don't score at all. Use both if you have access to both; they answer different questions.

**Why separate Future-Readiness from GEO instead of folding it in?**
Because they answer different questions: GEO asks "can AI systems cite you today," Future-Readiness asks "will today's fixes still matter as agent behavior keeps evolving." A site can score well on one and poorly on the other — collapsing them into one number would hide that.

**Can this fix issues automatically, like `claude-seo-ai`'s fixer?**
No, by design. It hands off a prioritized, owner-split action table (Developer actions / Content actions) rather than writing changes itself.

## Part of a small series

This is skill 1 of a small set of practitioner-built Claude Skills — [`sheet-cms-toolkit`](https://github.com/<your-username>/sheet-cms-toolkit) is skill 2, a zero-dependency validator for Google-Sheets-backed sites. More coming; star this repo to catch them.

## Author

Built by **Ahsan Jannat** — SEO, AEO & GEO specialist and Meta Ads consultant. More work at [ahsan-jannat.netlify.app](https://ahsan-jannat.netlify.app).

## License

MIT — see [LICENSE](./LICENSE). Use it, fork it, improve it.

## Keywords

Claude Skill, SEO audit, GEO audit, AEO audit, Generative Engine Optimization, Answer Engine Optimization, AI search visibility, AI crawler robots.txt, llms.txt, ChatGPT citations, Claude citations, Perplexity citations, AI-ready website, Claude Code skill, Claude Cowork skill, rendering risk audit, client-side rendering SEO
