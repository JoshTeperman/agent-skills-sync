---
name: principle-scope-checks-to-the-change
description: "Apply before a commit, a push, or a 'verify before done' step. Run only the checks that cover the change. Do not rerun a passing check, and do not default to the full test suite."
disable-model-invocation: true
---

# Scope checks to the change

Run only the checks that cover what you changed.

**Why:** Agents rerun the whole test suite before every commit, which wastes time and tokens. CI owns exhaustive coverage and the platform matrix.

## Guardrails

- Run targeted tests for the change, and the lint or type check for the files you touched.
- Do not rerun a check that already passed unless the code changed since that run.
- Leave the full suite and the platform matrix to CI.
- Run the full suite only when the user asks, there is no CI, or the change is cross-cutting.

This rule comes from DeepSeek's harness [AGENTS.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/AGENTS.md), as quoted in [Dave Kiss's post](https://x.com/davekiss/status/2122302114927870099).

Distinct from [Prove It Works](../principle-prove-it-works/SKILL.md), which checks that an output is real.
