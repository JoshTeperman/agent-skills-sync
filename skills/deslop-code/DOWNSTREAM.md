# Downstream: deslop-code

This skill is a fork of `deslop` from the Cursor `cursor-team-kit` plugin. This file records how the fork differs from upstream, so an agent can merge upstream updates without fetching the original first.

| | Upstream | Downstream |
|---|---|---|
| Source | [cursor/plugins `cursor-team-kit/skills/deslop`](https://github.com/cursor/plugins/blob/main/cursor-team-kit/skills/deslop/SKILL.md) | `skills/deslop-code` |
| Compared at | `6b78e9f` (2026-10-19) | `49c2a4b` |
| Name | `deslop` | `deslop-code` |
| Description | Remove AI-generated code slop and clean up code style | Remove AI-generated code slop and clean up code style. |
| Files | `SKILL.md` | `SKILL.md` |

## Changes

- RENAME `deslop` to `deslop-code`. The name pairs with `unslop-prose`, so each skill names the kind of text it cleans.
- PATCH frontmatter. Add `metadata.credits` and a trailing period on the description.
- PATCH the title from "Remove AI code slop" to "Deslop code".
- ADD a `## Downstream` section above the title.

The body, from "Check the diff against main" onward, is the same as upstream.
