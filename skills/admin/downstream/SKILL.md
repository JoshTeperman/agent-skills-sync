---
name: downstream
description: >-
  Keep an agent-managed record of downstream changes for a skill copied from another public repository, with attribution. Keep a record of changes and decisions so that updates to the upstream skill can be reconciled and merged to forked downstream path
disable-model-invocation: false
---

# Downstream

The referenced `DOWNSTREAM_SKILL` credits another author's skill, found at UPSTREAM_SOURCE_URL. Maintain a record of the forked changes compared to the original so that future changes to the original can be easily merged into the forked version.

## Steps
1. Create a `DOWNSTREAM.md` document at `DOWNSTREAM_PATH`, if it does not already exist. If it already exists, skip to 4.
2. Read the files in the original skill directory at `UPSTREAM_SOURCE_URL`, and compare to the forked files at `DOWNSTREAM_SKILL`, on current branch, including `description` from the downstream `SKILL.md`. File contents may be heavily amended, merged, or split into separate files, with new files or different directory structure. Assume any missing references to names, tools, other skills or files in the local version are intentional due to differing requirements.
3. Use your understanding from (2) and provide a list of local changes & ommissions with reason for the changes if available, so that any agent without context can understand the downstream skill without needing to fetch the upstream version, then skip to (5). Apply /unslop-prose to your answer. Format, contents (omit any if not relevant):
- Upstream vs Downstream columns in table format
- Descriptions from the SKILL.md
- Changes, Omissions
- Major renames or vocabulary differences
- File structures
4. Review changes on current branch for all files in directory at `DOWNSTREAM_PATH`, and read `DOWNSTREAM_PATH/DOWNSTREAM.md` to get up to date with historical changes. For any new changes, Add an entry to changes log, ordered by latest entry, descending. Apply /unslop-prose to each entry change summary. Each entry should include:
- Date
- Commit hash
- Change summary, pick from one of (`ADD`, `DELETE`, `PATCH`, `RENAME`) verbs, and describe the change. Use relative file paths.
5. Create a PR with /open-a-pr

## Metadata credits
Credits is available in calling skills metadata, and is a list of credits<author, url>.

```
metadata:
  credits:
    - author: Author One
      url: url_1
    - author: Author Two
      url: url_2
```

### UPSTREAM_OWNER
{metadata.credits.author}

### UPSTREAM_SOURCE_URL
{metadata.credits.url}

### DOWNSTREAM_SKILL
`name` of calling skill

### DOWNSTREAM_PATH
Defaults to working directory of calling skill, or `skills/{DOWNSTREAM_SKILL}` with skill name dash-separated.



