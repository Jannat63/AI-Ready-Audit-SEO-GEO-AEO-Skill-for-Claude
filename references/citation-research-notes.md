# Citation Research Notes

The scoring rubric isn't a checklist someone invented — it's built on this research. If a report's findings get pushback ("why does this matter?"), the answer is in here. Keep this file updated as better research appears; don't let it go stale the way most competing skills' assumptions have.

## Citation patterns across AI platforms

- Wikipedia accounts for the largest single share of ChatGPT's top citations (measured around 48%), while Reddit shows up much more heavily in Gemini and Perplexity citations specifically — platform choice for off-site presence should follow which AI system actually matters most to the target audience, not a one-size-fits-all list.
- A large-scale 2026 benchmark analysis (Conductor, spanning roughly 13,800 domains, ~22 million searches, and ~17 million AI responses) found ChatGPT responsible for the large majority of AI-referral traffic, with AI-referral conversions running roughly double the rate of traditional search referrals — the traffic is smaller in volume than classic search but converts meaningfully better.

## What actually moves the needle (and what doesn't)

- Schema.org/JSON-LD structured data has a real but modest effect: an Ahrefs test across roughly 1,900 pages found only about a 2.4% lift in AI Mode citation from adding schema markup. Worth doing — cheap and technically correct — but don't oversell it as a major lever in a report.
- Third-party presence matters more than most on-page work: domains active on review platforms (G2, Capterra, Trustpilot, Yelp) showed roughly 3x higher odds of AI citation; domains with real community activity on Reddit/Quora showed roughly 4x higher odds. For developer-facing brands specifically, GitHub, Product Hunt, Stack Overflow, and Hacker News presence plays the equivalent role.
- Spreading the same expertise across multiple credible third-party publications rather than only publishing on the brand's own site has been associated with a large increase (cited around 3x) in AI citation likelihood compared to owned-site-only publishing.
- Most brands are starting from zero: an estimated 90% of brands currently have no measurable AI search presence at all, which is as much an opportunity framing as a warning.

## Technical / structural findings

- Google discontinued FAQ rich results in classic search for all sites as of May 7, 2026. FAQPage schema no longer earns a Google SERP payoff — it may still help an AI system parse Q&A structure, but that's a different justification and the report should say which one applies.
- `llms.txt` adoption is real (Anthropic, Stripe, Vercel, Cloudflare, and others publish one) but actual consumption is unproven at scale — one widely-cited measurement found the large majority of published files got zero fetch requests in a recent month. The best-documented consumers are developer-tool AI agents (Claude Code, Cursor, Windsurf) reading documentation sites, not general AI chat/search citation.
- GitHub itself is a domain both Claude and ChatGPT draw on for technical queries — relevant context for treating a well-documented public repository as a legitimate piece of an AI-visibility strategy, not only a coding artifact.

## Sources

- Conductor — 2026 AEO/GEO Benchmarks Report
- Ahrefs — schema markup / AI Mode citation lift study, referenced via `199-biotechnologies/claude-skill-seo-geo-optimizer` statistics reference
- amplifying-ai/awesome-generative-engine-optimization (GitHub) — collected AI platform citation pattern research and agency GEO methodology summaries
- Kulbhushan Pareek — "50 Websites LLMs Cite Most: The AI Link Building List (2026)"
- Wellows — LLM SEO / GEO framework guide (2026)
- JDM Web Technologies — LLM SEO Guide (2026)
- Contextbolt, Sourceable (Medium), and llmstxt.org-derived guides — llms.txt spec and adoption/consumption data
- AgriciDaniel/claude-seo (GitHub) — Google's FAQ rich-result deprecation timeline and current schema.org guidance

Update this file when better or more recent primary research is available — a rubric grounded in 2026 numbers should get revisited periodically, the same way the skill asks every audited site to keep its own content fresh.
