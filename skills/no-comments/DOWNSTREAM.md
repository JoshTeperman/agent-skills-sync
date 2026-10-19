# Downstream: no-comments

This skill is a fork of `no-comments` by Lauren Tan (@poteto), with the `comment-sicko` subagent persona merged in. This file records how the fork differs from upstream, so an agent can merge upstream updates without fetching the original first.

| | Upstream | Downstream |
|---|---|---|
| Source | [cursor/plugins `pstack/skills/no-comments`](https://github.com/cursor/plugins/blob/main/pstack/skills/no-comments/SKILL.md) | `skills/no-comments` |
| Compared at | `6b78e9f` (2026-10-19) | `49c2a4b` |
| Name | `no-comments` | `no-comments` |
| Description | Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints. | fix unnecessary comments, and offer encodings for claimed constraints |
| Files | `SKILL.md`, plus the `comment-sicko` agent definition elsewhere in the plugin | `SKILL.md` |

## Changes

- PATCH frontmatter. Add `metadata.credits`. Drop "Spawn Comment Sicko" from the description, because downstream does not spawn a subagent.
- ADD a `## Downstream` section above the title.
- DELETE the opening lines "Spawn Comment Sicko. Act on accepted findings." and "Defer to Comment Sicko's fresh perspective."
- PATCH step 1. Upstream spawns a `Task` with `subagent_type: "comment-sicko"`. Downstream analyses the scope with the Comment Sicko persona in the same agent and returns its report.
- PATCH step 2. Upstream runs `/how` or `/why` on thin `IMPORTANT` or `do not remove` comments. Downstream reports them as `unclear` for the user to review. Downstream also drops the rule to revert and rerun a rejected report, and to fail `/no-comments` on a second rejection.
- PATCH step 3. Upstream runs `/architect` for fixes that need a shape. Downstream fixes trivial flags and writes a note with a best-guess root-cause fix for the rest.
- DELETE step 4, which implemented the smallest root-cause fix in scope under `principle-fix-root-causes` and `principle-redesign-from-first-principles`. Downstream leaves larger fixes as notes.
- PATCH step 5 (now 4). "Leave keeps" becomes "Leave notes".
- PATCH step 6 (now 5). The report drops reruns and the architect sketch, and adds root-cause notes from step 3.
- ADD a `## Comment Sicko` section with the persona, its keep list, kill targets, and report format. Upstream keeps this in a separate agent definition.
- PATCH the persona. Unclear `IMPORTANT` claims get the mark `unclear` instead of a `/how` or `/why` run.

## Vocabulary

| Upstream | Downstream |
|---|---|
| Spawn Comment Sicko | Analyse with the Comment Sicko persona |
| keeps | notes |

## Change log

### 2026-10-19 · #4

- PATCH `SKILL.md`. Point `metadata.credits.url` to upstream `no-comments` instead of `how`.
- PATCH `SKILL.md`. Step 5 reports root-cause notes instead of reruns and an architect sketch.
