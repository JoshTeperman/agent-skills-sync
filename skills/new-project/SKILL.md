---
name: new-project
description: Create a new project in the project store from the current conversation. Use for "/new-project <instructions>", e.g. "/new-project create new project 'My Project' from our conversation".
disable-model-invocation: true
---

# New Project

## Setup
1. Read `config.yaml`.
2. Read `providers/<provider>.md` for the `provider` in `config.yaml`. Use it for all store operations. If the provider or its file is missing, list the files in `providers/` and ask the user to update `config.yaml` or generate a provider file for the new store.

## Steps

### 1. Name
Take the project name from the prompt. If missing or unclear, ask. Never derive one.

### 2. Check for duplicates
List and read every project under `projects_root` in project store. If one looks like a duplicate, pause and confirm with the user what they would like to do. Provide multiple choice question, not free text. One option should be Cancel.

### 3. Sub-agent
If the tool can create agents or sub-agents, ask the user if they would like to create one. If yes, create one named after the project with:

```
- Read the whole project (README and every doc) before acting.
- Append new decisions to `decisions-log.md`.
- Keep project docs current as the work changes.
- Ask before going beyond the project's scope.
```

### 4. Create project in project store
Path: `<projects_root>/<project_name>`

Include in the project:
- `README.md`: With sections `Description`, `Purpose`
- `decisions-log.md`: only if decisions exist. Per entry: date, decision, rationale.
- One doc per existing plan, PRD, architecture doc, etc. from the conversation, in full.

Apply the **unslop** skill to each line.

**Name conventions generic.** Use "the user" or "the human" in imperatives, not the author's first name.

### 5. Report
Provide project name, project link, sub-agent handover status (created / not supported).

## Guardrails
- Use only conversation content. Don't invent decisions or docs.
- Never overwrite or update an existing project without confirmation.
