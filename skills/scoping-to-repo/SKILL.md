---
name: scoping-to-repo
description: >-
  Promote a ready project-store scoping page into a GitHub repo as the
  source of truth: docs/scoping.md, CLAUDE.md, and the docs/changes/ and
  docs/specs/ layout. Use for "/scoping-to-repo <project-name>".
disable-model-invocation: true
---

# Scoping to repo

Promote a ready `scoping` page from Notion into the project's GitHub repo. After this, `docs/scoping.md` is the source of truth. Use the Notion MCP tools (`notion-search`, `notion-fetch`, `notion-update-page`). Plain nested pages only, no databases.

## Steps

### 1. Project, readiness, repo
Take the project name from the prompt. If missing or unclear, ask. Never derive one.

Search for a page titled `Projects`. Find the child page named `<project-name>`, then its child titled `scoping`. Fetch `scoping` in full. If it is already a stub that points at a repo copy, stop and say so.

Confirm the doc is ready: planned spikes or MVPs are done (findings written back) or the user says to promote anyway. If it is not ready, stop.

Identify the GitHub repo from the prompt, the appendix, or by asking. Inspect whatever already exists (a mid-scope spike may have created the repo ad-hoc) and work with that state. If there is no repo yet, create it only after the user confirms, then clone or init locally. Don't commit or push the scoping files unless the user asks.

If `docs/scoping.md` or `CLAUDE.md` already exists, confirm before overwriting.

Supporting docs are siblings or children of `scoping`. Leave them in place.

### 2. Write `docs/scoping.md`
Normalise the store page into clean markdown at `docs/scoping.md`:

- Keep sections 0–11 and every heading. Keep `N/A — <reason>` bodies.
- Keep testable requirement IDs, checkbox state, and grouping.
- Keep the Section 10 milestone table and its status column.
- Keep the Section 11 decision index (`S-D#`, and `<###>-D#` when change decisions already exist).
- Drop store-only chrome (tool markup, duplicate "how this document is used" wording that only applies to the store). In the "source of truth" note, say the repo copy now wins.

Apply the **unslop** skill. Don't invent or drop decisions, requirements or milestones.

### 3. Write `CLAUDE.md`
Create `CLAUDE.md` at the repo root from `templates/CLAUDE.md.tmpl`. Fill the project name and a one-line summary from Section 0. Do not invent workflow rules beyond the template. If you also created `docs/changes/README.md`, add that the roadmap there is approved as written and a scope change needs a new proposal.

### 4. Scaffold `docs/changes/` and `docs/specs/`
Create `docs/changes/archive/` and `docs/specs/` (empty is fine; specs are written when changes complete).

For each applicable Section 10 milestone except the scoping/design row itself, create `docs/changes/<###-name>/` with:

- `proposal.md` — why, what changes, out of scope, a Decisions section (number them `D1`, `D2`, …; the index cites them as `<###>-D#`, for example `004-D2`), and how we know it worked. Leave decisions and evidence blank unless they are already in scoping.
- `tasks.md` — ordered steps and done-criteria, from the milestone when present.
- Do not create `results.md` yet. It is written when the change completes (measurements, and screenshots or GIFs when the change touches a frontend).

If a later milestone is still unclear because of an upstream dependency, still scaffold the folder and note that exception explicitly in `proposal.md` / `tasks.md`. Don't invent the missing details.

Use zero-padded folder names (`001-mvp`). If Section 10 already numbers milestones, keep those numbers and slug the name. Confirm with the user if the mapping is unclear.

Create `docs/changes/README.md` only if the project has multiple tracks, many milestones, or planned parallel work. If you do, make it the roadmap (order, tracks, dependencies). Do not invent dates.

### 5. Stub the store page
After the repo files are written, convert the Notion `scoping` page to a short stub that links to the repo's `docs/scoping.md` (and the repo URL if known). Confirm first. Supporting docs stay in Notion as children; do not delete them.

`notion-update-page` `replace_content` with a short stub:

- The repo copy is now the source of truth.
- Link to `docs/scoping.md` in the repo (full GitHub URL if known, otherwise the repo path).
- New decisions and scope changes go in the repo (`docs/scoping.md`, `docs/changes/`).
- Supporting docs can stay as child pages.

Preserve every child page and child database tag from the fetch. If the tool says children would be deleted, show the list and ask before retrying with `allow_deleting_content`. Never set that flag without confirmation.

### 6. Report
Paths written, change folders created, whether a changes README was added, store stub link, and that `docs/scoping.md` is now the source of truth. Say if nothing was committed or pushed.

## Guardrails
- Don't invent requirements, decisions, milestones or dates.
- Confirm before overwriting existing repo files or replacing the store `scoping` page.
- Never delete supporting docs or child pages without confirmation.
- Don't force-push, don't commit or push, and don't open a PR unless the user asks.
- Don't edit the scoping template in the store.
