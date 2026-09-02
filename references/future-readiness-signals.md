# Future-Readiness Signals

This is the dimension most competing audit skills don't measure at all. It exists because SEO, GEO, and AEO all answer "is this working right now" — and AI crawling behavior is changing fast enough that "right now" is a moving target. This file separates what's confirmed from what's a reasonable bet, because a report that blurs the two isn't trustworthy.

## Why this dimension is defensible, not just a marketing angle

Three things have already happened, not might happen:

1. **Crawlers split into categories within the last year or two.** OpenAI, Anthropic, and Perplexity all now run separate training / search-index / user-fetch bots instead of one crawler per company. A robots.txt written with one blanket AI rule is already behind this — it can't express "let them cite me, don't let them train on me," which is a distinction real site owners increasingly want to make.

2. **IDE and coding agents fetch documentation directly.** Claude Code, Cursor, Windsurf, GitHub Copilot, and Aider all look for `llms.txt`/`llms-full.txt` when working against a documentation site and route to the linked pages from there. This is live, observable agent behavior today, not speculation — it's just not something classic SEO or GEO audits check for, because it's a different consumer (a coding agent, not a search feature).

3. **The retrieval pattern is shifting from "index the whole page" to "fetch exactly the section needed."** Modular, cleanly-sectioned content survives this better than long monolithic pages, independent of any AI-specific optimization — it's just how structured retrieval works.

## What's confirmed vs. emerging — keep these separate in the report

**Confirmed, check for it directly:**
- Crawler-tier granularity in robots.txt (see `ai-crawler-directory.md`)
- Whether core content/navigation requires JS execution to exist at all (compounds directly with the SEO rendering-risk check — an agent that can't run JS can't act on a page any more than a search crawler can index it)
- Structured data depth (bare Organization schema vs. product/article/service/FAQ-specific types where relevant to the content)
- Any freshness or versioning signal at all (dated content, changelogs, "last updated" markers)
- Content modularity — can a single page section stand alone and make sense if an agent fetched only that section, or does it depend on reading the whole page top to bottom

**Emerging — flag as a plausible direction, not a settled fact:**
- Agent-to-agent content/commerce exchange patterns (early and speculative as of the sources this rubric draws on)
- `llms.txt` adoption broadening beyond documentation sites to general brand content
- Structured-data vocabularies extending beyond current schema.org norms

## How to write this into a report

Don't say "you need this for 2027." Say what's actually true: "this specific thing is already live and checkable today, here's the evidence, and it happens to be under-measured by every other SEO/GEO audit because it's newer than the checklist most of them were written against." That's a more credible claim than a vague future-proofing pitch, and it's the same underlying idea stated honestly.
