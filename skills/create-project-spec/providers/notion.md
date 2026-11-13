# Provider: Notion

Use the Notion MCP tools (`notion-search`, `notion-fetch`, `notion-create-pages`, `notion-duplicate-page`, `notion-move-pages`, `notion-update-page`).
Plain nested pages only, no databases.

```
Projects/
  <project_name>/
    README.md
    scoping
    <supporting docs>
  scoping-template
```

`projects_root` and `scoping_template` are page titles in `config.yaml`. Resolve them with `notion-search` by title or path. If several matches, prefer a page under the Projects root. If still ambiguous, ask.

## Find root
Search for a page titled `projects_root`. Several matches: prefer the Projects root by path; if still ambiguous, ask which one. None: ask whether to create it and under which parent. Create it only after they confirm.

## List projects
Fetch the root. Direct child pages are candidates. Skip `scoping-template` and pages that are clearly not projects (for example a Planning docs grouping or an Archived toggle). Fetch a candidate if the name might be a duplicate.

## Create project
Create page `<project_name>` under the root. Leave its body empty. Return the project page URL.

## Create scoping
1. Search for a page titled `scoping_template`. Prefer a child of the Projects root if several match; ask if still ambiguous.
2. `notion-duplicate-page` on that page. Duplication is async and lands next to the template, not under the project. Do not treat the returned URL as ready until a fetch shows the template headings.
3. `notion-move-pages` the duplicate under the project page.
4. `notion-update-page` `update_properties` to set the title to `scoping`.
5. Never edit the template page itself.

## Fill scoping
`notion-update-page` `update_content` for settled sections (smallest exact `old_str`). Keep every heading. For unused Sections 2–8, replace the section body (not the heading) with `N/A — <reason>`. Preserve child pages.
