# Scoring Rubric

Every audit produces four scores, each 1–10. Don't eyeball these — work through the checklist below for each one and add up the points. If you deduct or award a point, the report should say why in one clause, not just show the number.

Read `citation-research-notes.md` alongside this file — it's the evidence these thresholds are built on. If a client or reader asks "says who?" about any score, that file has the answer.

---

## SEO (1–10) — traditional crawlability and on-page foundation

Start at 10, subtract:

| Finding | Deduction |
|---|---|
| `rendering_risk.level` = high (page is effectively a blank shell to a crawler that doesn't execute JS) | −4 |
| `rendering_risk.level` = medium | −2 |
| No `sitemap.xml`, or present but unparseable | −1.5 |
| Standard search crawlers (Googlebot) blocked or path-scoped-restricted in robots.txt without clear reason | −2 |
| `h1_count` ≠ 1 (zero H1s or multiple competing H1s) | −1 |
| Missing `<title>` or meta description | −1 (each, max −1.5 combined) |
| No canonical tag on a site with any URL parameter or duplicate-path risk | −0.5 |

A site with zero deductions is a genuine 10 — don't invent a deduction to avoid giving a perfect score. Most real sites land 5–8.

## GEO (1–10) — AI-citation readiness

Start at 10, subtract:

| Finding | Deduction |
|---|---|
| Major AI search-index or user-fetch bots blocked (`OAI-SearchBot`, `Claude-SearchBot`, `Claude-User`, `PerplexityBot`, `Perplexity-User`) — this directly removes the site from AI answers, not just training | −3 (any one blocked), −5 (multiple blocked) |
| No `llms.txt`, or present but not spec-compliant shape | −1 (don't over-weight this — see the honest caveat in `llms-txt-guide.md`; its measured impact is closer to a low-cost hedge than a proven lever) |
| No JSON-LD structured data anywhere on scanned pages | −2 |
| No Organization/brand entity schema (name, description, `sameAs` links to verified profiles) | −1 |
| Web-search check finds no third-party footprint at all on platforms AI systems cite heavily for the industry (Reddit, LinkedIn, Wikipedia, relevant review platforms) | −2 |
| Only AI *training* bots blocked, search/user-fetch bots allowed | −0.5 (minor — this is a legitimate content-licensing choice many sites make on purpose; note it, don't penalize it hard) |

Blocking search/user-fetch bots is the single highest-leverage negative finding in this whole rubric — it's a direct, verifiable reason a site cannot appear in AI answers, independent of content quality. Always lead with this if found.

## AEO (1–10) — direct-answer readiness

This one needs judgment on the fetched page content, not just the script output. Start at 10, subtract:

| Finding | Deduction |
|---|---|
| Key pages open with marketing copy/mission statements instead of a direct answer to the obvious visitor question | −2 |
| No FAQ content or Q&A-structured sections anywhere on the scanned pages | −1.5 |
| No visible freshness signal (dates, "last updated", versioned content) on content that should be time-sensitive | −1 |
| No named authorship or credentials on content that makes expertise claims (guides, comparisons, technical claims) | −1.5 |
| Claims made without any supporting source, data, or specificity ("industry-leading quality" with nothing backing it) | −1 |
| Headings don't map to the questions a reader actually has (generic "Our Services" instead of specific, answerable headings) | −1 |

Note on FAQPage schema specifically: Google stopped showing FAQ rich results for all sites as of May 7, 2026, so FAQPage markup no longer has a Google rich-result payoff. It can still help AI systems parse Q&A structure semantically — don't recommend it for Google rich results, but it's fine to recommend for AI parsing if the content genuinely is Q&A-shaped. Say which reason applies.

## Future-Readiness (1–10) — is the site built for where this goes next, not just where it is

Start at 10, subtract. Be explicit in the report about which of these are **confirmed current behavior** vs. **emerging pattern** — don't blur the two.

| Finding | Deduction | Status |
|---|---|---|
| robots.txt treats all AI bots as one blanket rule instead of distinguishing training/search-index/user-fetch categories | −2 | Confirmed — this distinction is live and controllable today |
| Content structure is monolithic (huge single pages mixing many topics) rather than modular sections an agent could fetch and use independently | −1.5 | Confirmed pattern, forward-leaning value |
| No structured data beyond a bare minimum (e.g., only basic Organization, nothing product/article/service-specific where relevant) | −1.5 | Confirmed |
| No freshness/versioning mechanism at all (no dates anywhere, no changelog, no last-modified signal) | −1.5 | Confirmed — recency weighting is already a factor and likely to matter more |
| `llms.txt` absent on a site with substantial documentation or reference content | −1 | Emerging — flag as low-cost hedge, not urgent |
| Site requires JS execution for core navigation (compounds with the SEO rendering-risk finding — an agent that can't execute JS can't act on the site at all) | −2 | Confirmed |

Always include one sentence in the report distinguishing this score from GEO: GEO measures "can AI systems cite you today," Future-Readiness measures "will today's fixes still matter as agent behavior keeps evolving." They usually move together but not always — a site can be well-optimized for today's GEO checklist while still being architecturally brittle for what's coming.

---

## Overall presentation

Report all four scores together, never collapse them into one number — the whole point of separating them is that a site can be strong on one and weak on another, and that's the useful information. If asked for "one score," give the average but keep the breakdown visible.
