# Downstream: grilling

This skill is a fork of `grilling` by Matt Pocock. This file records how the fork differs from upstream, so an agent can merge upstream updates without fetching the original first.

| | Upstream | Downstream |
|---|---|---|
| Source | [mattpocock/skills `skills/productivity/grilling`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) | `skills/grilling` |
| Compared at | `49dd158` (2026-10-09) | `49c2a4b` |
| Name | `grilling` | `grilling` |

Both descriptions are the same: "Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases."

## File structure

```diff
 grilling/
 ├── SKILL.md
-└── agents/openai.yaml
+└── DOWNSTREAM.md
```

## Changes

- PATCH frontmatter. Add `metadata.credits` for the upstream author.
- ADD a `## Downstream` section and a `# Grilling` title above the body.

The body is the same as upstream.

## Omissions

- `agents/openai.yaml`. It sets the display name "Grilling" and the short description "Stress-test thinking a round of questions at a time" for OpenAI agent clients. Downstream does not target those clients.
