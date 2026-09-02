# llms.txt — Spec and Honest Guidance

Don't oversell this file in a report. It's worth recommending because it's nearly free to implement and has no downside — but be straight with the reader about what it does and doesn't do.

## What it is

A plain Markdown file served at the domain root (`/llms.txt` — nowhere else, must be exactly this path and filename). Proposed by Jeremy Howard (Answer.AI / fast.ai) in September 2024 as a way to hand AI systems a curated, low-noise map of a site's most useful pages, instead of making them parse full HTML pages full of navigation, scripts, and cookie banners.

It is a community convention, not a standard backed by any recognized standards body. There is no enforcement mechanism and no guarantee any given AI system reads it.

## The format

```markdown
# Site or Project Name

> A one-paragraph blockquote summary — the single sentence you'd use
> to explain what this is and who it's for.

Optional free-form context paragraph. No headings in this section.

## Docs

- [Page name](https://example.com/page): One-line description of what's there
- [Another page](https://example.com/another): What it covers

## Examples

- [Example](https://example.com/example): One-line context

## Optional

- [Less critical link](https://example.com/extra): Skippable under tight context
```

Rules that separate a valid file from a broken one:
- Exactly one H1, and it must be the first line
- The blockquote directly under the H1 is the only other structurally-parsed element — everything else is free-form
- Absolute `https://` URLs only, every link should return a clean 200
- Served as plain UTF-8 Markdown text, not HTML
- Curated, not comprehensive — practical guidance across multiple implementers converges on roughly 3–5 sections and 10–20 links total. A dump of the entire sitemap is the most common implementation mistake and defeats the purpose.
- A separate `/llms-full.txt` is the recommended companion for cases where a fuller single-file version is useful (e.g., an agent that wants the whole thing in one fetch rather than following links).

## The honest caveat — say this in every report that recommends it

As of the sources this rubric is built on: no major AI lab (OpenAI, Anthropic, Google, Meta) has publicly and consistently committed to reading or acting on `llms.txt` in production systems. One widely-cited measurement found that the large majority of published `llms.txt` files received zero fetch requests in a given month. The clearest, best-documented consumers today are developer-tool AI agents — Claude Code, Cursor, Windsurf, GitHub Copilot, Aider — which fetch `llms.txt`/`llms-full.txt` when working against a documentation site, not general-purpose chat/search citation.

This means: recommend it for sites with real documentation or technical reference content, where IDE-agent consumption is the most plausible payoff. Don't frame it as a general AI-citation lever for a typical business site — that overstates current evidence. The honest pitch is "costs you almost nothing, plausible upside for developer-facing content, zero downside" — not "this will get you cited by ChatGPT."

## What the scan checks

`technical_scan.py`'s `llms_txt` block reports presence and a structural shape check (H1 present, blockquote present, section/link counts) — it does not and cannot verify whether any AI system is actually fetching the file. Don't claim it does.
