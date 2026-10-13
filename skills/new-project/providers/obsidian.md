# Provider: Obsidian

Use file system tools.
Requires `vault_path: /path/to/vault` in `config.yaml`. If unset, ask the user for the path and add it.

## Find root
`<vault_path>/<projects_root>/`. If missing, ask before creating.

## List projects
Each subfolder is a project. Read its `README.md`.

## Create project
1. Create folder `<project_name>/` with `README.md`, `decisions-log.md` (if any), one `.md` per other doc.
2. Return the folder path.
