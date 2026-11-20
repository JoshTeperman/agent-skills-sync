# agent-skills-sync

Reusable agent skills in the `SKILL.md` format, shared across agent tools, and the command-line tools they use.

- `skills/` holds skills. A skill is a folder with a `SKILL.md` (YAML frontmatter `name` + `description`, then instructions) and any supporting files. Skill folders can sit at any depth, such as `skills/principles/<skill-name>/`.
- `capabilities/` holds tools, one folder per capability, such as `capabilities/<capability-name>/`. A capability is a plain CLI that prints JSON or text, so any agent, script, or person can call it. A skill tells agents when and how to call a capability, and doesn't copy its code.

### Setup

Run these once in each clone:

```sh
git config core.hooksPath .githooks
bin/link
```

### Syncing skills and capabilities

`bin/link` creates symlinks and is safe to re-run. The git hooks run it again when a pull changes `skills/`, `capabilities/`, or `bin/`.

- Every folder under `skills/` that has a `SKILL.md` is linked into each target as `<target>/<folder-name>`, because agent tools find skills one level deep only. The default target is `~/.claude/skills`.
- Every executable file directly inside `capabilities/<capability-name>/` is linked as a command into `$CAPABILITIES_BIN`, default `~/.local/bin`. The command name is the file name without its extension, with `_` replaced by `-`, so `yt_transcript.py` becomes `yt-transcript`. `bin/link` warns if that folder isn't on `PATH`.
- Links to deleted skills and capabilities are removed. A real file or folder, or a link that points outside this repo, is left alone with a warning. If two skills or two commands have the same name, the shallower path wins, then the first path in alphabetical order. `bin/link` warns about the one it skips.

```sh
bin/link                                                  # link into the default targets
bin/link --dry-run                                        # show what would change
bin/link ~/.claude/skills ~/.agents/skills                # custom skill targets
SKILLS_TARGETS="$HOME/.claude/skills $HOME/.agents/skills" bin/link
CAPABILITIES_BIN="$HOME/bin" bin/link                     # custom command folder
```

<details>
<summary>All skills</summary>

| skill | description |
|---|---|
| [`/new-project`](./skills/new-project/SKILL.md) | create a project in your project store (Notion by default) from the current conversation. |
| [`knowledge-vault`](./skills/knowledge-vault/SKILL.md) | search and read the user's knowledge vault over its tailnet-only MCP server (native MCP or `curl`). |
| [`youtube-transcript`](./skills/youtube-transcript/SKILL.md) | fetch a YouTube video's transcript from its captions with the `yt-transcript` command. |

</details>
