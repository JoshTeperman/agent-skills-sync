---
name: create-skill
description: Draft PR to add new agent skill to local (current project) or global shared skills repository.
disable-model-invocation: true
---

# Create Skill

## Flow

### 0.1 Skill scope
Scope: Default to global unless user specifies 'local'.

If scope is `local`, continue to next step.
If scope is `global`, move to shared skills project directory at `~/#{projects_directory}/#{shared_skills_repository_name}`. If the project is not found, clone the repo at the expected path and pull latest before continuing from the shared skills project directory.

### 0.2. Check for an existing skill
Name: Take from the prompt. If missing or unclear, ask. Never derive or guess the name.

Look recursively for an existing skill with the same name or that seems like a duplicate.
If `global` scope, look in `./skills/**/*`.
If `local`, directory name may differ depending on the provider, eg`.claude/skills/**/*`, `.cursor/skills/**/*`, `.agents/skills/**/*`.
Skills can live in sub folders inside the `/skills` directories, not just at top level.

Continue if no existing skill is found, else ask the user what they would like to do with a multiple-choice question, not free-text, and include a Cancel option.

### 1. Draft the skill
Frontmatter:
- description: Ask the user to describe the skill, it's purpose, and when it should trigger. Keep as one YAML scalar. Quote it or use `description: >-` with indented continuation lines when punctuation or wrapping requires it.
- disable-model-invocation: `true` by default, set to `false` only if the user wants to allow the model or other workflows to trigger the skill.

Apply the **unslop** skill to every line.

Show the draft to the user and take feedback. Expect multiple iterations. Cut ruthlessly. A skill is not a manual.

### 2. Finalise
Work in a worktree off main. Commit and open a PR. Don't push to main directly.

### 3. Wrap up
Always return to the original project working directory.
