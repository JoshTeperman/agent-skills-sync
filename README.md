# agent-skills-sync

Reusable agent skills in the `SKILL.md` format, shared across agent tools.

Each skill lives in `skills/<skill-name>/` with a `SKILL.md` (YAML frontmatter `name` + `description`, then instructions) and any supporting files.

## Usage

Clone this repo once and symlink `skills/*` (or the whole `skills/` folder) into each tool's skills directory, then `git pull` to update.

## Skills

- `new-project` – create a project in your project store (Notion by default) from the current conversation.
