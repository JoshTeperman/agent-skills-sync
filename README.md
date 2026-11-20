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

### Skills

| skill | description |
|---|---|
| [`agent-router`](./skills/agent-router/SKILL.md) | Triage and route new messages in the agent email inbox either as action items or knowledge to be sent directly to the knowledge agent. |
| [`create-project-spec`](./skills/create-project-spec/SKILL.md) | Create and fill a project's scoping doc in the project store. |
| [`create-skill`](./skills/create-skill/SKILL.md) | Create a PR to add new agent skill to local (current project) or global shared skills repository. |
| [`deslop-code`](./skills/deslop-code/SKILL.md) | Remove AI-generated code slop and clean up code style. |
| [`downstream`](./skills/admin/downstream/SKILL.md) | Keep an agent-managed record of downstream changes for a skill copied from another public repository, with attribution. |
| [`execution-time`](./skills/execution-time/SKILL.md) | Entry point skill for writing considered, principled code, unslopped prose, and verified work. |
| [`grilling`](./skills/grilling/SKILL.md) | Grill the user relentlessly about a plan, decision, or idea. |
| [`how`](./skills/how/SKILL.md) | Use for "how does X work", code walkthroughs before changing something, and placement, ownership, or layering questions. |
| [`knowledge-vault`](./skills/knowledge-vault/SKILL.md) | Search and read the user's knowledge vault, a read-only MCP server on their tailnet. |
| [`new-project`](./skills/new-project/SKILL.md) | Create a new project in the project store from the current conversation. |
| [`no-comments`](./skills/no-comments/SKILL.md) | Fix unnecessary comments, and offer encodings for claimed constraints. |
| [`open-a-pr`](./skills/open-a-pr/SKILL.md) | Open a pull request. |
| [`scoping-to-repo`](./skills/scoping-to-repo/SKILL.md) | Promote a ready project-store scoping page into a GitHub repo as the source of truth. |
| [`technical-writing`](./skills/technical-writing/SKILL.md) | Layered technical-writing standard: Diátaxis structure, Google developer style sentences, STE instruction rules, Global English syntax. |
| [`unslop-prose`](./skills/unslop-prose/SKILL.md) | Cut AI tells from any writing. |
| [`youtube-transcript`](./skills/youtube-transcript/SKILL.md) | Fetch the transcript of a YouTube video from its captions. |

### Principles

| skill | description |
|---|---|
| [`principle-attack-the-premise`](./skills/principles/principle-attack-the-premise/SKILL.md) | Apply when two or more fixes that share one premise have failed the same gate. |
| [`principle-boundary-discipline`](./skills/principles/principle-boundary-discipline/SKILL.md) | Apply when wiring validation, error handling, or framework adapters. |
| [`principle-build-the-lever`](./skills/principles/principle-build-the-lever/SKILL.md) | Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, or checks. |
| [`principle-encode-lessons-in-structure`](./skills/principles/principle-encode-lessons-in-structure/SKILL.md) | Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. |
| [`principle-exhaust-the-design-space`](./skills/principles/principle-exhaust-the-design-space/SKILL.md) | Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. |
| [`principle-experience-first`](./skills/principles/principle-experience-first/SKILL.md) | Apply when product, UX, or feature-scope tradeoffs come up. |
| [`principle-explain-the-number`](./skills/principles/principle-explain-the-number/SKILL.md) | Apply before you trust, report, or act on a number you measured. |
| [`principle-fix-root-causes`](./skills/principles/principle-fix-root-causes/SKILL.md) | Apply when debugging. Trace each symptom to its root cause and fix it there. |
| [`principle-foundational-thinking`](./skills/principles/principle-foundational-thinking/SKILL.md) | Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. |
| [`principle-guard-the-context-window`](./skills/principles/principle-guard-the-context-window/SKILL.md) | Apply when context is filling up: large outputs, long files, repeated reads, or fan-out planning. |
| [`principle-laziness-protocol`](./skills/principles/principle-laziness-protocol/SKILL.md) | Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. |
| [`principle-make-operations-idempotent`](./skills/principles/principle-make-operations-idempotent/SKILL.md) | Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. |
| [`principle-migrate-callers-then-delete-legacy-apis`](./skills/principles/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | Apply when introducing a new internal API while old callers still exist. |
| [`principle-minimize-reader-load`](./skills/principles/principle-minimize-reader-load/SKILL.md) | Apply when reviewing or shaping code that's hard to trace. |
| [`principle-model-the-domain`](./skills/principles/principle-model-the-domain/SKILL.md) | Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files. |
| [`principle-never-block-on-the-human`](./skills/principles/principle-never-block-on-the-human/SKILL.md) | Apply when tempted to ask 'should I do X?' on reversible work. |
| [`principle-outcome-oriented-execution`](./skills/principles/principle-outcome-oriented-execution/SKILL.md) | Apply during planned rewrites and migrations with explicit phase boundaries. |
| [`principle-prove-it-works`](./skills/principles/principle-prove-it-works/SKILL.md) | Apply after completing a task, before declaring done. |
| [`principle-redesign-from-first-principles`](./skills/principles/principle-redesign-from-first-principles/SKILL.md) | Apply when integrating a new requirement into an existing design. |
| [`principle-separate-before-serializing-shared-state`](./skills/principles/principle-separate-before-serializing-shared-state/SKILL.md) | Apply when concurrent actors might write to the same file, branch, key, or state object. |
| [`principle-sequence-verifiable-units`](./skills/principles/principle-sequence-verifiable-units/SKILL.md) | Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. |
| [`principle-subtract-before-you-add`](./skills/principles/principle-subtract-before-you-add/SKILL.md) | Apply when sequencing an addition, refactor, or rewrite. |
| [`principle-test-behavior-not-implementation`](./skills/principles/principle-test-behavior-not-implementation/SKILL.md) | Apply when you write, change, or keep a test. |
| [`principle-type-system-discipline`](./skills/principles/principle-type-system-discipline/SKILL.md) | Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. |

</details>
