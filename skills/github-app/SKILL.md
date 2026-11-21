---
name: github-app
description: >-
  Act on GitHub (gh and git: clone, fetch, push, commits, PRs, issues, comments, reviews) as the
  GitHub App's bot, with a short-lived token scoped to one repository. Use for every GitHub call,
  instead of plain gh or git and instead of any personal credentials.
---

# GitHub as the app bot

The `github-app` command gets a token from the token service on the user's tailnet, limited to one repository and the permissions you ask for, then runs `gh` or `git` with it. Your work shows on GitHub as `<app-slug>[bot]`, so the user can review and merge it like anyone else's. Every token request is logged with the machine and the agent name you give.

There's no setup. Each call carries everything it needs, and nothing is written to git config.

## Rules

1. **Use the wrappers for every GitHub call.** `github-app gh` for every `gh` command, and `github-app git` for every git command that talks to github.com and for commits you'll push there. Never call plain `gh` or `git` against GitHub, and never use personal credentials or tokens.
2. **Ask for the minimum.** Name exactly the repository the task is about, and use `--permission-profile read` unless you'll write.
3. **Identify yourself every time.** End every PR body, issue and comment with this line, and add it to every commit message as a trailer:

   ```
   Agent: <agent-name> (<provider>, <model>)
   ```

4. **Stop on errors.** If the command reports that the service is unreachable or returns an error, stop and tell the user. Don't retry with other credentials.
5. **Protect tokens.** Never echo, log or commit a token.

## Options (same for every subcommand)

| option | |
|---|---|
| `--repository OWNER/NAME` | Required. Never inferred from the current directory. |
| `--permission-profile read` | contents, pull_requests and issues read, plus metadata read. |
| `--permission-profile write` | contents, pull_requests and issues write, plus metadata read. |
| `--permissions '<json>'` | Anything else, e.g. `'{"contents":"read","checks":"read"}'`. Values are `read` or `write`. |
| `--agent-name NAME` | Required. Falls back to `$AGENT_NAME`. |
| `--agent-provider`, `--agent-model`, `--purpose` | Optional. Fall back to `$AGENT_PROVIDER`, `$AGENT_MODEL`, `$AGENT_PURPOSE`. |

Exactly one of `--permission-profile` and `--permissions` is required.

## Examples

```sh
R=JoshTeperman/agent-skills-sync
ME=(--agent-name master-chief --agent-provider grok-bot --agent-model grok-4)

github-app gh  --repository $R --permission-profile read  "${ME[@]}" -- pr list
github-app git --repository $R --permission-profile read  "${ME[@]}" -- clone https://github.com/$R.git

cd agent-skills-sync
git switch -c fix-typo   # local-only git commands need no wrapper
github-app git --repository $R --permission-profile write "${ME[@]}" -- commit -am "Fix typo" -m "Agent: master-chief (grok-bot, grok-4)"
github-app git --repository $R --permission-profile write "${ME[@]}" -- push -u origin fix-typo
github-app gh  --repository $R --permission-profile write "${ME[@]}" --purpose "typo fix PR" -- \
  pr create -R $R --title "Fix typo" --body $'Fixes a typo.\n\nAgent: master-chief (grok-bot, grok-4)'
```

- Use `https://github.com/...` remotes. The helper answers only for HTTPS github.com and only for the `--repository` you named, so a push to any other repository fails.
- Commits made through `github-app git` are authored and committed by the bot.
- `github-app token <options>` prints a bare token on stdout, for a tool that isn't `gh` or `git`. Pass it straight to that tool; never print it.

Tokens last an hour and are cached in `~/.cache/gh-token-service/` until 5 minutes before they expire.

## Service URL

The command finds the service at `https://vps.<tailnet>.ts.net/github-token`, reading the tailnet name from `tailscale status`. To override it, set `GITHUB_TOKEN_SERVICE_URL` in the environment or in `.env` in this skill folder (see `.env.example`). The service is reachable only from the user's tailnet.
