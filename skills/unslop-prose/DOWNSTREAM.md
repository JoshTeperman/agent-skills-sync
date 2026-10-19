# Downstream: unslop-prose

This skill is a fork of `unslop` by Lauren Tan (@poteto). This file records how the fork differs from upstream, so an agent can merge upstream updates without fetching the original first.

| | Upstream | Downstream |
|---|---|---|
| Source | [cursor/plugins `pstack/skills/unslop`](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md) | `skills/unslop-prose` |
| Compared at | `6b78e9f` (2026-10-19) | `49c2a4b` |
| Name | `unslop` | `unslop-prose` |
| Description | Cut AI tells from any writing. | Cut AI tells from any writing. |
| Files | `SKILL.md` | `SKILL.md` |

## Changes

- RENAME `unslop` to `unslop-prose`. The name pairs with `deslop-code`, so each skill names the kind of text it cleans.
- PATCH frontmatter. Add `metadata.credits` for the upstream author.
- ADD a `## Downstream` section and a paragraph that points readers to this file before any upstream merge.
- PATCH rule numbers. Upstream numbers its rules 3 to 33 with gaps, because upstream deletes rules and keeps the numbers as stable ids. Downstream renumbers them 1 to 28 with no gaps. The downstream numbers are now the stable ids, so a rule removed downstream leaves a gap. The rule text is the same, except that rule 27 cites rule 21 for metaphor nouns instead of rule 26.

## Rule number map

Other skills cite rules by number. Use this map to translate an upstream citation.

| Upstream | Downstream | Rule |
|---|---|---|
| 3 | 1 | Superficial -ing phrases |
| 5 | 2 | Vague attributions |
| 7 to 12 | 3 to 8 | Language rules |
| 13 to 19 | 9 to 15 | Style rules |
| 20 | 16 | Chatbot phrases |
| 22 | 17 | Sycophantic tone |
| 23 to 25 | 18 to 20 | Filler rules |
| 26 | 21 | Abstract metaphor nouns |
| 27 to 33 | 22 to 28 | Plain speech rules |
