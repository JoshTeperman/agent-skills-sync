---
name: new-project
description: Create a new project in the project store (Notion by default) from the current conversation, including a description, a decisions log, and any docs already written. Use when the user says "/new-project", "create a new project", or similar, with optional free-text instructions such as the project name.
---

# New Project

Turns the current conversation into a new project in the project store.

Input: free-text instructions, e.g. `/new-project create new project from our conversation, call it project-terrific`.

## Setup

1. Read `config.yaml` in this skill folder. `provider` names the project store; `projects_root` names the Projects directory (default `Projects`).
2. Read `providers/<provider>.md` and use its instructions for every store operation below (list, read, create). If the file doesn't exist, tell the user which providers are available and stop.

## Steps

### 1. Work out the project name
- Use the name given in the instructions if there is one ("call it X", "named X").
- Otherwise derive a short, descriptive name from the conversation.
- If you can't tell, ask the user. Keep the name as given; for folder-style stores use a kebab-case slug.

### 2. Check for duplicates
- List every existing project under `projects_root` and read each one's description.
- If any looks like a duplicate (same or similar name, or same purpose), tell the user which one and why, and **stop until they confirm** whether to continue, rename, or update the existing project instead.

### 3. Create a sub-agent
- If the current tool can create agents or sub-agents, create one named after the project, briefed with the project description and a pointer to the project's location in the store.
- If it can't, say so plainly (e.g. "This tool can't create sub-agents, so I skipped that step") and continue. Never skip silently.

### 4. Create the project in the store
Create `<projects_root>/<project_name>` containing:
- **Description** (`README.md` or the page body): what the project is, what it does, goals, and current status.
- **`decisions-log.md`**: only if decisions have already been made. One entry per decision with date, decision, rationale, and alternatives considered if discussed.
- **Other existing docs**: any plan, PRD, architecture doc, or similar already written in the conversation, each as its own document, copied in full. Don't invent documents that weren't written.

### 5. Report
Tell the user the project name, its location/link in the store, the documents created, and the sub-agent result (created or not supported).

## Rules
- Only use content from the conversation; don't make up decisions or plans.
- Don't overwrite an existing project without explicit confirmation.
