# Provider: Obsidian

Obsidian vaults are plain folders of markdown files. Use file system tools.

## Locate the Projects root
- The vault path must be known (ask the user, or add `vault_path:` to `config.yaml`).
- The Projects root is `<vault_path>/<projects_root>/`. If it doesn't exist, ask the user before creating it.

## List and read existing projects
- Each subfolder of the Projects root is a project; read its `README.md`.

## Create the project
- Create `<projects_root>/<project-name>/` with `README.md` (description), `decisions-log.md` (if any decisions), and one `.md` file per other existing document (e.g. `plan.md`, `prd.md`, `architecture.md`).
- Return the folder path.
