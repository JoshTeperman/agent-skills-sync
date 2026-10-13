# Provider: Notion

Use the Notion MCP tools (`notion-search`, `notion-fetch`, `notion-create-pages`).
Plain nested pages only, no databases. Each file is a child page, so the tree exports to markdown.

```
Projects/
  <project_name>/
    README.md
    decisions-log.md
    <other docs>
```

## Find root
1. Search for a page titled `projects_root`.
2. Several matches: ask which one.
3. None: ask the user whether to create it and under which parent. Create it only after they confirm.

## List projects
Fetch the root. Each child page is a project. Fetch its `README.md` child page.

## Create project
1. Create page `<project_name>` under the root. Leave its body empty.
2. Create child pages: `README.md`, `decisions-log.md` (if any), one per other doc.
3. Return the project page URL.
