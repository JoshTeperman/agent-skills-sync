# Downstream: open-a-pr

This skill merges three upstream sources into one skill that opens a PR and writes its body. This file records how the fork differs from each source, so an agent can merge upstream updates without fetching the originals first.

| | Upstream | Downstream |
|---|---|---|
| Sources | [mattpocock/skills `skills/engineering/pr`](https://github.com/mattpocock/skills/blob/main/skills/engineering/pr/SKILL.md) by Matt Pocock, at `49dd158` (2026-10-09) | `skills/open-a-pr` at `49c2a4b` |
| | [humanlayer/skills `plugins/show-me/skills/show-me`](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) by Dex Horthy, at `653b641` (2026-10-08) | |
| | [cursor/plugins `pstack/skills/poteto-mode/playbooks/opening-a-pr.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md) by Lauren Tan (@poteto), at `6b78e9f` (2026-10-19) | |
| Names | `pr`, `show-me`, and the "Opening a PR" playbook | `open-a-pr` |
| Descriptions | `pr`: "Use when writing a PR body." `show-me`: "Help the user understand the current topic visually with concise diagrams, code-shape sketches, and focused HTML artifacts." | Open a pull request |
| Invocation | `show-me` sets `disable-model-invocation: true` | `disable-model-invocation: false` |

## File structure

```diff
-pr/
-├── SKILL.md
-├── CREDITS.md
-└── agents/openai.yaml
-show-me/
-├── SKILL.md
-└── agents/openai.yaml
-poteto-mode/playbooks/opening-a-pr.md
+open-a-pr/
+├── SKILL.md
+└── DOWNSTREAM.md
```

## Where each part comes from

| Downstream section | Source |
|---|---|
| Worktree, Commits, PRs, Titles, Descriptions, Size and stacks, Readiness | `opening-a-pr.md` |
| Description sections `## Evidence` and `## Blast Radius` | `pr` |
| Visual Aids | `show-me`, by way of `pr` |

## Changes from `opening-a-pr.md`

- PATCH PRs. `/deslop` from `cursor-team-kit` becomes `/deslop-code`, and `/unslop` becomes `/unslop-prose`. Drop "every layer except Diátaxis" from the `/technical-writing` instruction.
- PATCH Titles. The example scopes `pstack` and `poteto-mode` become `Knowledge Vault` and `Math Tutor UI`, and scope can be "the area, project, or epic name".
- PATCH Worktree. Drop "Subagents inherit it."
- PATCH Descriptions. `## What changed` points to Visual Aids. `## Blast Radius` drops the line about the cost of leaving main red. `## Verification` drops the link to arena or swarm results and the ban on methodology and metric tables. Add `## Evidence` from `pr`.
- PATCH Size and stacks and Readiness. Drop the Origin `--status open` and `origin pr ready` paths, and the reference to `playbooks/shipping.md`.

## Changes from `pr`

- PATCH the body template. The `## Summary`, `## Evidence`, and `## Merge Danger` template becomes the `opening-a-pr.md` section list. Evidence keeps its S-tier and A-tier guidance. Blast Radius moves from Merge Danger to its own section.

## Changes from `show-me`

- PATCH the component tree code fence from `tsx` to `text`.
- PATCH the `expandSkill` example to end statements with semicolons.

## Omissions

- `opening-a-pr.md` Forge section, which picks `origin` over `gh` when available. Downstream uses `gh`.
- `opening-a-pr.md` Built-in PR tool section, which routes PR operations through a run's built-in tool.
- `pr` Merge Danger one-way or two-way door rating.
- `pr` instruction to use domain language from `GLOSSARY.md`.
- `pr` and `show-me` Guidance on placing each visual next to its text and not using every visual type.
- `show-me` focused HTML file option for dense UI or layout visuals.
- `pr/CREDITS.md`. `metadata.credits` replaces it.
- `agents/openai.yaml` from `pr` and `show-me`. Downstream does not target OpenAI agent clients.

## Vocabulary

| Upstream | Downstream |
|---|---|
| `/deslop` | `/deslop-code` |
| `/unslop` | `/unslop-prose` |
| Summary | Visual Aids, used inside What changed |
| Merge Danger | Blast Radius |
