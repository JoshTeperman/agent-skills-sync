# Provider: Obsidian

Use file system tools.
Requires `vault_path: /path/to/vault` in `config.yaml`. If unset, ask the user for the path and add it.
`projects_root_id` is Notion-only; ignore it.

## Find project and scoping
`<vault_path>/<projects_root>/<project_name>/scoping.md`. Read it in full. If it is already a stub pointing at the repo copy, stop.

Supporting docs in the same folder stay in the vault.

## Stub scoping
After the repo files exist, confirm with the user, then replace the body of `scoping.md` with a short stub that links to the repo's `docs/scoping.md`. Do not delete other files in the project folder.
