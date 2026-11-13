# Provider: Obsidian

Use file system tools.
Requires `vault_path: /path/to/vault` in `config.yaml`. If unset, ask the user for the path and add it.
`projects_root_id` and `scoping_template_id` are Notion-only; ignore them.

Optional: `scoping_template_path` in `config.yaml`, an existing markdown file to copy.

## Find root
`<vault_path>/<projects_root>/`. If missing, ask before creating.

## List projects
Each subfolder is a project. Skip a folder named `scoping-template`.

## Create project
Create folder `<project_name>/`. Do not invent a `README.md`. Return the folder path.

## Create scoping
Path: `<vault_path>/<projects_root>/<project_name>/scoping.md`.

If `scoping_template_path` is set, copy it. Otherwise create `scoping.md` with the section headings from the skill, in order, and empty bodies. Never overwrite an existing `scoping.md` without confirmation.

## Fill scoping
Edit `scoping.md` in place as rounds settle. Keep every heading. For unused Sections 2–8, replace the body with `N/A — <reason>`.
