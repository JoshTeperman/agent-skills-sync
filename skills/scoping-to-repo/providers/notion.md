# Provider: Notion

Use the Notion MCP tools (`notion-search`, `notion-fetch`, `notion-update-page`).
Plain nested pages only, no databases.

```
Projects/
  <project_name>/
    scoping
    <supporting docs>
```

`projects_root` is the page title. `projects_root_id` is in `config.yaml`. Prefer the ID when set.

## Find project and scoping
1. If `projects_root_id` is set, fetch that page; otherwise search for `projects_root`.
2. Find the child page named `<project_name>`, then its child titled `scoping`.
3. Fetch `scoping` in full. If the body is already a stub pointing at `docs/scoping.md`, stop.

Supporting docs are siblings or children of `scoping`. Leave them in place.

## Stub scoping
After the repo files exist, confirm with the user, then `notion-update-page` `replace_content` with a short stub:

- The repo copy is now the source of truth.
- Link to `docs/scoping.md` in the repo (full GitHub URL if known, otherwise the repo path).
- New decisions and scope changes go in the repo (`docs/scoping.md`, `docs/changes/`).
- Supporting docs can stay as child pages.

Preserve every child page and child database tag from the fetch. If the tool says children would be deleted, show the list and ask before retrying with `allow_deleting_content`. Never set that flag without confirmation.
