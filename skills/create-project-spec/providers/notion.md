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

`projects_root` is the page title. `projects_root_id` and `scoping_template_id` are in `config.yaml`. Prefer the IDs when set.

## Find root
1. If `projects_root_id` is set, fetch that page.
2. Otherwise search for a page titled `projects_root`. Several matches: ask which one. None: ask whether to create it and under which parent. Create it only after they confirm.

## List projects
Fetch the root. Direct child pages are candidates. Skip `scoping-template` and pages that are clearly not projects (for example a Planning docs grouping or an Archived toggle). Fetch a candidate if the name might be a duplicate.

## Create project
Create page `<project_name>` under the root. Leave its body empty. Return the project page URL.

## Create scoping
1. `notion-duplicate-page` on `scoping_template_id`. Duplication is async and lands next to the template, not under the project. Do not treat the returned URL as ready until a fetch shows the template headings.
2. `notion-move-pages` the duplicate under the project page.
3. `notion-update-page` `update_properties` to set the title to `scoping`.
4. Never edit the template page itself.

## Fill scoping
`notion-update-page` `update_content` for settled sections (smallest exact `old_str`). Keep every heading. For unused Sections 2–8, replace the section body (not the heading) with `N/A — <reason>`. Preserve child pages.
