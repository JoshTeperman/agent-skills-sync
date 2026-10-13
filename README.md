# agent-skills-sync

Reusable agent skills in the `SKILL.md` format, shared across agent tools.

Each skill lives in `skills/<skill-name>/` with a `SKILL.md` (YAML frontmatter `name` + `description`, then instructions) and any supporting files.

## Usage

Clone this repo once and symlink `skills/*` (or the whole `skills/` folder) into each tool's skills directory, then `git pull` to update.

## Skills

- `new-project` – create a project in your project store (Notion by default) from the current conversation.

## Linking

```sh
bin/link              # link into default targets
bin/link --dry-run    # show what would change
bin/link ~/a ~/b      # custom targets
SKILLS_TARGETS="~/a ~/b" bin/link
```

Default target: `~/.claude/skills`. Each skill is linked individually. Re-run after `git pull`; safe to repeat. Links to deleted skills are removed.

**Local vs synced:** a real folder in a target dir is a local skill and is never touched (a warning is printed). A symlink into this repo is a synced skill.
