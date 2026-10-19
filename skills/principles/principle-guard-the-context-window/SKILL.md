---
name: principle-guard-the-context-window
description: "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Suggest routing bulk to subagents; keep summaries in the main thread, not raw payloads."
disable-model-invocation: true
---

# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.

### Routing bulk to subagents
In cases where there is a large amount of exploratory or discovery work that would bloat context, suggest a plan to route or handoff that work to subagents. Any handoff work should be broken up into distinct pieces where it can return a concrete answer that can be summarised and merged with the context in the main thread.
