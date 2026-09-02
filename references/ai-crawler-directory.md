# AI Crawler Directory

`scripts/technical_scan.py` checks robots.txt against every bot in this table automatically. This file explains what each one actually does, because "allow or block everything" is the wrong mental model — the categories matter more than the individual names.

## The three categories

**Training bots** — crawl content to build future model training datasets. Blocking one costs nothing in today's AI citations; it only affects what future model versions know about the site.

**Search-index bots** — build the retrieval index an AI system's live answers are assembled from. Blocking one of these is the closest thing to a direct "don't show me in AI answers" switch.

**User-fetch bots** — fire in real time when an actual person's question triggers a live page fetch. Blocking these means the site can't be pulled into an answer even when a user is asking about it right now.

The practical rule: blocking training bots is a legitimate content-licensing choice with no visibility downside. Blocking search-index or user-fetch bots directly removes a site from AI answers. Most sites that accidentally block AI visibility do it by using one blanket rule (`User-agent: *` / `Disallow: /` for anything AI-flavored) instead of choosing per-category.

## The table

| User-agent | Operator | Category | Notes |
|---|---|---|---|
| `GPTBot` | OpenAI | Training | Highest-volume AI crawler by most traffic measurements |
| `OAI-SearchBot` | OpenAI | Search-index | Powers ChatGPT's search/answer sourcing |
| `ChatGPT-User` | OpenAI | User-fetch | Fires when a ChatGPT user triggers a live browse |
| `ClaudeBot` | Anthropic | Training | |
| `Claude-SearchBot` | Anthropic | Search-index | |
| `Claude-User` | Anthropic | User-fetch | |
| `PerplexityBot` | Perplexity | Search-index | Perplexity has been reported running non-compliant/stealth crawling in some cases — treat robots.txt as necessary but not sufficient here |
| `Perplexity-User` | Perplexity | User-fetch | |
| `Google-Extended` | Google | Training | Controls Gemini/Vertex AI training use specifically. Does **not** affect classic Google Search or Search AI Overviews — those run through `Googlebot`, which should almost never be blocked |
| `Googlebot` | Google | Search-index | Do not block unless the intent is genuinely to disappear from Google Search entirely — this also removes AI Overviews / AI Mode visibility since both route through this crawler |
| `Applebot-Extended` | Apple | Training | |
| `Amazonbot` | Amazon | Training | |
| `meta-externalagent` | Meta | Training | |
| `Bytespider` | ByteDance | Training | Documented history of partial/non-compliance with robots.txt — a Disallow rule is a first line of defense, not a guarantee |
| `CCBot` | Common Crawl | Training | Nonprofit open web archive; widely used as a training source by many labs beyond just its own operator, including early GPT, Llama, and Mistral generations |
| `Diffbot` | Diffbot | Training | |

## Reading the scan output

`technical_scan.py` reports each bot as `allowed_site_wide: true/false` plus `has_path_scoped_rules_to_review: true/false`. A `true` on the second field means the site has more nuanced rules than a blanket allow/block — worth reading the actual robots.txt directly before concluding anything, since the script deliberately doesn't try to resolve full path-precedence logic (that's a judgment call, not a fact to automate).

## What to recommend

Don't default to "allow everything" or "block everything" as a template answer — it depends on what the site owner actually wants (AI training-data participation is a real choice some site owners want to opt out of regardless of citation impact). What the report should always flag clearly: if search-index or user-fetch bots are blocked and the client's stated goal includes AI visibility, that's a direct contradiction worth surfacing prominently, not a minor technical note.
