# Downstream: how

This skill is a fork of `how` by Lauren Tan (@poteto). This file records how the fork differs from upstream, so an agent can merge upstream updates without fetching the original first.

| | Upstream | Downstream |
|---|---|---|
| Source | [cursor/plugins `pstack/skills/how`](https://github.com/cursor/plugins/blob/main/pstack/skills/how) | `skills/how` |
| Compared at | `6b78e9f` (2026-10-19) | `49c2a4b` |
| Name | `how` | `how` |
| Files | `SKILL.md`, `references/explainer-prompt.md`, `references/explorer-prompt.md` | Same files |

Both descriptions are the same. The description starts "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions".

## Changes

- PATCH frontmatter. Add `metadata.credits` for the upstream author.
- ADD a `## Downstream` section above the title.
- PATCH `references/explainer-prompt.md`. The first instruction says the explorer findings "may" include overlapping angles. Upstream says each explorer always investigated a different angle. Downstream can run one explorer, so the explainer must not expect several.
- PATCH `references/explorer-prompt.md`. Add a blank first line. This change has no effect.

## Omissions

- The paragraph on subagent spawn settings. Upstream spawns every subagent as `generalPurpose` and `readonly`, and takes model slugs from the Cursor rule `pstack-models.mdc` (defaults `grok-4.7-xhigh-fast` for explorers and `claude-opus-5-5-xhigh` for explainers). It also links reasoning level and speed to the Subagents section of `poteto-mode`. Downstream does not run in Cursor and its `execution-time` skill has no Subagents section, so the agent picks subagent settings itself.
