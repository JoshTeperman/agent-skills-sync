---
name: new-project
description: Create a new project in the project store (Notion by default) from the current conversation. Use for "/new-project <instructions>", e.g. "/new-project create new project from our conversation, call it project-terrific".
disable-model-invocation: true
---

# New Project

## Setup
1. Read `config.yaml`.
2. Read `providers/<provider>.md`. Use it for all store operations. If missing, list available providers and stop.

## Steps
1. **Name.** Take the project name from the prompt. If missing or unclear, ask. Never derive one.
2. **Duplicates.** List and read every project under `projects_root`. If one looks like a duplicate, tell the user and stop until they confirm.
3. **Sub-agent.** If the tool can create agents or sub-agents, create one named after the project with the briefing below. If not, say so plainly.
4. **Create** `<projects_root>/<project_name>` with:
   - `README.md`: what the project is and does, goals, status.
   - `decisions-log.md`: only if decisions exist. Per entry: date, decision, rationale.
   - One doc per existing plan, PRD, architecture doc, etc. from the conversation, in full.
5. **Report** name, location/link, docs created, sub-agent result.

## Sub-agent briefing
- Read the whole project (README and every doc) before acting.
- Append new decisions to `decisions-log.md`.
- Keep project docs current as the work changes.
- Ask before going beyond the project's scope.

## Rules
- Use only conversation content. Don't invent decisions or docs.
- Never overwrite an existing project without confirmation.
