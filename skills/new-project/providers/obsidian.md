# Provider: Obsidian

Use file system tools. Vault: `vault_path` from `config.yaml`. If unset, ask.

## Find root
`<vault_path>/<projects_root>/`. If missing, ask before creating.

## List projects
Each subfolder is a project. Read its `README.md`.

## Create project
1. Create folder `<project_name>/` with `README.md`, `decisions-log.md` (if any), one `.md` per other doc.
2. Return the folder path.
