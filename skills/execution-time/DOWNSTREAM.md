# Downstream: execution-time

This skill is a fork of `poteto-mode` by Lauren Tan (@poteto). This file records how the fork differs from upstream, so an agent can merge upstream updates without fetching the original first.

| | Upstream | Downstream |
|---|---|---|
| Source | [cursor/plugins `pstack/skills/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) | `skills/execution-time` |
| Compared at | `6b78e9f` (2026-10-19) | `49c2a4b` |
| Name | `poteto-mode` | `execution-time` |
| Description | poteto's agent style for concise, detailed responses, deliberate subagents, unslopped prose, simple code, and verified work. Use for poteto, /poteto-mode, or requests to work in this style. | entry point skill for writing considered, principled, code, unslopped prose and verified work |

## File structure

```diff
-poteto-mode/
+execution-time/
 ├── SKILL.md
-├── playbooks/      # 22 playbooks
-├── references/bugbot-triage.md
-└── scripts/        # bootstrap, check-plan, orch, watch-pr, worktree-audit
+└── DOWNSTREAM.md
+playbooks/
+└── investigate.md
```

The downstream playbook lives at `skills/playbooks/investigate.md`, outside the skill directory. The skill tells the agent to open playbooks at `playbooks/<title>.md` relative to the skill, so that path does not resolve.

## Changes

- RENAME `poteto-mode` to `execution-time`. The skill is an entry point for serious work, not a personal style.
- PATCH frontmatter. Add `metadata.credits`. Drop the `icon` and `color` keys.
- ADD a `## Downstream` section and an intro that routes serious programming work through this skill.
- PATCH Principles. Three summaries differ from upstream:
  - Attack the Premise. Downstream: "Take a census of which actors hold the imbalance before the next fix, then question the premise". Upstream: "Write the premise down and test it directly".
  - Fix Root Causes. Downstream: "Trace each symptom to its root cause, reproduce first, ask why until you reach it." Upstream: trace each symptom to the first place the system went wrong, and a guard is a fix only when the state it handles is legitimate.
  - Test Behavior, Not Implementation. Downstream: call the code as its users do, assert against a literal expected value, and rewrite or delete a test that passes when every import returns `undefined`. Upstream: assert what users can observe, so the test fails on broken behavior and passes on internal changes.
- ADD four downstream playbooks: Investigate, Grill with docs, Create spec, and Implement. Only Investigate has a file. Grill with docs and Create spec have no description.
- PATCH the upstream playbook list. Mark all upstream playbooks DISABLED until they merge into the local skills.
- DELETE the figure-it-out and Orchestrate routing paragraph from Playbooks.
- PATCH Pause safely. "a Cursor restart" becomes "a Cursor/Claude restart".

## Omissions

- "Bundled skills live at `../<name>/SKILL.md`" and the instruction to pass this file's path to every `poteto-agent` prompt.
- Non-negotiables. This includes the rule to name each principle that shaped a decision, and every trigger: how, prototype before asking, data shape first, architect, swarm and arena, interrogate, throughput checkpoint, unslop, technical-writing, deslop, no-comments, control skills, benchmark-checklist, Babysit, Shipping, bugbot triage, broken-skill fixes, and show-me-your-work. Most of these skills do not exist downstream.
- Subagents. This includes the `poteto-agent` subagent type, `Task` defaults, per-role model slugs from `/setup-pstack`, reasoning level and speed rules, and fresh-subagent-by-default. These depend on Cursor and pstack tooling.
- All 22 upstream playbook files, `references/bugbot-triage.md`, and `scripts/`.

## Vocabulary

| Upstream | Downstream |
|---|---|
| `poteto-mode` | `execution-time` |
| Investigation playbook | Investigate playbook |

## Known issues

- Writing the reply cites "unslop rule 14" for colon overuse. In `unslop-prose`, that rule is 10.
- Writing the reply and the Investigate playbook name the `unslop` skill. Downstream, that skill is `unslop-prose`.
