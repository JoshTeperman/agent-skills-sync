# Provider: Notion

Use the Notion connector (MCP) tools, typically `notion-search`, `notion-fetch`, and `notion-create-pages` (names may vary slightly by client).

## Locate the Projects root
1. Search Notion for a page or database titled `projects_root` (from `config.yaml`, default `Projects`).
2. If several match, ask the user which one to use.
3. **If none exists**, tell the user and ask whether to create it and where (workspace top level or under a given parent page). Don't create it without confirmation. Create it as a plain page unless the user prefers a database.

## List and read existing projects
- Fetch the Projects page/database and list its child pages (or database entries).
- Fetch each child to read its description for the duplicate check.

## Create the project
1. Create a child page of the Projects root titled `<project_name>`, with the project description as its body. (If the root is a database, create an entry and set the title property.)
2. Under that page create a child page `decisions-log.md` (title `Decisions Log` is also fine) if there are decisions.
3. Create one child page per other existing document (e.g. `Plan`, `PRD`, `Architecture`), with the content in Notion markdown.
4. Return the project page URL.
