# agent-skills-sync

Reusable agent skills in the `SKILL.md` format, shared across agent tools.

Each skill lives in `skills/<skill-name>/` with a `SKILL.md` (YAML frontmatter `name` + `description`, then instructions) and any supporting files.

### Setup

Clone this repo and configure your hooks path so hooks in `/.githooks` are active.

```bash
git config core.hooksPath .githooks`
```

### Syncing Skills

Skills in `/skills` are synced to all specified directories with symlinks. Run the `bin/link` script to generate the symlinks. Defaults to `~/.claude/skills`, but you can specify custom targets. Safe to re-run. Re-runs `bin/link` when a git pull changes `skills/`. Links to deleted skills are removed, and symlink is skipped when local skill with the same name already exists.

```sh
bin/link              # link into default targets
bin/link --dry-run    # show what would change
bin/link ~/.claude/skills ~/.agents/skills      # custom targets
SKILLS_TARGETS="~/.claude/skills ~/.agents/skills" bin/link # configure with env var
```

<details>
<summary>All skills</summary>

| skill | description |
|---|---|
| [`/new-project`](./skills/new-project/SKILL.md) | create a project in your project store (Notion by default) from the current conversation. |

</details>

