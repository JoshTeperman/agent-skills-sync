---
name: create-project-spec
description: >-
  Create and fill a project's scoping doc in the project store. Use for
  "/create-project-spec <project-name>", or when starting project scoping
  before a repo exists.
disable-model-invocation: true
---

# Create project spec

Create and fill `scoping` under `<projects_root>/<project-name>/` in the project store.

`new-project` creates the project folder and `README.md`. This skill creates or fills `scoping`. When scoping is ready, `scoping-to-repo` promotes it into the GitHub repo as the source of truth.

## Setup
1. Read `config.yaml`.
2. Read `providers/<provider>.md` for the `provider` in `config.yaml`. Use it for all store operations. If the provider or its file is missing, list the files in `providers/` and ask the user to update `config.yaml` or generate a provider file for the new store.

## Steps

### 1. Name
Take the project name from the prompt. If missing or unclear, ask. Never derive one.

### 2. Find or create the project
List projects under `projects_root`. Skip the scoping template and other non-project pages the provider names.

- No match: create `<project-name>` under the root. Do not invent a `README.md` or other docs; that is `new-project`.
- Exact or similar match: confirm with a multiple-choice question, including Cancel. Never overwrite an existing project without confirmation.
- If `scoping` already exists: ask whether to fill the existing page, leave it, or cancel. Never overwrite it without confirmation.

### 3. Create `scoping` if needed
If it does not exist, clone the configured scoping template as `<projects_root>/<project-name>/scoping`. Keep every heading. Do not edit the template itself.

### 4. Interview and fill
Use the **grilling** skill: design tree in rounds, whole frontier each round, recommended answers, wait for the user's replies.

Start the tree at **Section 0** and **Section 1** only. Do not interview Sections 2–8 until Section 1 shows they apply. Then open only the sections that apply. Mark unused sections `N/A — <reason>`. Never delete a heading.

Always fill **Sections 9–11** once 0 and 1 are settled (and 2–8 are filled or marked N/A). Section 10 lists only milestones that apply, plus a spike/MVP row when exploration is still needed.

Write settled rounds back to the `scoping` page as you go. Apply the **unslop** skill. Use "the user" or "the human" in imperatives, not the author's first name.

### 5. Decisions, estimates, size
- Number scoping decisions `S-D#` and record them in full in Section 11 (Decision Log & Index). Append only; mark superseded rows, do not delete them.
- No time estimates unless the user gives deadlines. If they do, record those dates only — do not invent effort or schedules.
- Trim process overhead for small projects: keep 0, 1, 10 and 11 tight; settle 2–8 with short N/A reasons rather than a full interview of every subsection.
- Leave room for exploratory spikes or MVPs. Scoping is not ready for `scoping-to-repo` while a planned spike is still open, unless the user says it is ready anyway. Write spike findings back into the relevant sections (especially 0 and 1) when they land.

### 6. Report
Project name, scoping link, which sections are filled vs `N/A`, open spike/MVP status, and whether the user has called the doc ready for `scoping-to-repo`.

## Sections
Keep these headings, in this order, matching the scoping template:

- **0. Project Summary** — Problem; Why it matters / impact; Proposed approach; Primary success metric; Key risks / unknowns
- **1. Problem Framing & Success Metrics** — Business / User Problem (who, pain, why an AI approach or not); Goal; Prior Work; Input and Output; Data Storage; Scope (v1 In-Scope, Out-of-Scope, Deferred); Constraints; Success Metrics (user-facing, technical, system); Requirements (testable behaviour, stable IDs such as `R1`, `U1`); Checklist
- **2. Prompt Engineering & Systematic Tracking**
- **3. Model Selection & Evaluation**
- **4. RAG Implementation**
- **5. Agent Systems**
- **6. Deployment & User Interface**
- **7. System Monitoring & Error Analysis**
- **8. Fine-Tuning (Optional / Advanced)**
- **9. Code Quality & Repository Structure**
- **10. Milestones** — dependency order and done-criteria, no invented dates
- **11. Appendix** — links, diagrams, glossary, Decision Log & Index

## Guardrails
- Use only what the user said or what is already in the store. Don't invent requirements, decisions, metrics or deadlines.
- Never overwrite an existing project or `scoping` page without confirmation.
- Never edit or overwrite the scoping template.
- Don't run `scoping-to-repo` from this skill.
