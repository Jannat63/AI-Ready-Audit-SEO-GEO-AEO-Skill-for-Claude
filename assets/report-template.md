# Report Template

Use this structure for the downloadable report (docx/pdf). Fill every section — don't skip "What's already working," it's what makes the priorities credible instead of just a list of problems.

---

```
[Site Name] — AI-Ready Audit
[Audit type: Quick / Full]  |  [Date]  |  Prepared by [name/brand]

## Executive Summary
Three to five sentences: what this site does, the headline finding (usually
the single biggest technical or structural issue found), and the overall
shape of the four scores. No jargon here — this section should be readable
by someone with zero SEO background.

## Scores

| Dimension | Score | One-line why |
|---|---|---|
| SEO | X/10 | |
| GEO (AI-citation readiness) | X/10 | |
| AEO (direct-answer readiness) | X/10 | |
| Future-Readiness | X/10 | |

## What's Already Working
Two to four specific, verified strengths. Not generic praise — name the
actual thing found (e.g., "robots.txt already splits AI crawlers by
category — most sites don't do this yet").

## Findings by Dimension

### SEO
[Evidence-backed findings from the technical scan, each tied to the specific
deduction it triggered in the rubric. Include the actual numbers — visible
text ratio, script tag count, sitemap URL count — don't just assert a
conclusion.]

### GEO
[Same pattern. Include the robots.txt crawler table for this site if any
bot is blocked, and the results of the third-party footprint check.]

### AEO
[Content-quality findings — this section leans on judgment more than the
others, so be specific about which page and which passage.]

### Future-Readiness
[State plainly which findings here are confirmed current behavior vs.
emerging pattern — pull the distinction from
references/future-readiness-signals.md rather than blurring it.]

## Priority Actions

Split by owner — most real fixes need both, and this split is what
actually gets things assigned and shipped.

### Developer Actions
| # | Action | Why it matters | Effort |
|---|---|---|---|
| 1 | | | |

### Content / SEO Actions
| # | Action | Why it matters | Effort |
|---|---|---|---|
| 1 | | | |

## Methodology Note
This audit was produced using only Claude's native web search and fetch
tools plus a standard-library Python scan — no third-party SEO API or paid
subscription was used to generate it. Scoring method: [link or reference
to scoring-rubric.md]. Scanned on [date] — website content changes, and an
audit is a snapshot, not a permanent state.
```

---

## In-chat summary (send this before the file, always)

Keep this to what fits on one screen:

```
[Site] — AI-Ready Audit (Quick/Full)

SEO  X/10   GEO  X/10   AEO  X/10   Future-Ready  X/10

Biggest strength: [one sentence, specific]

Top 3 priorities:
1. [specific, named finding — not "improve SEO"]
2. [specific, named finding]
3. [specific, named finding]

Full report with the complete breakdown and action tables: [attached]
```
