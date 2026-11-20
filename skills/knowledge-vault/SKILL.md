---
name: knowledge-vault
description: >-
  Search and read the user's knowledge vault, a read-only MCP server on their tailnet. Use before
  answering or researching anything the user may already have notes, decisions, or sources on, and
  whenever the user says "check the vault" or asks what they know or decided about something.
disable-model-invocation: false
---

# Knowledge vault

The vault is the user's external brain: wiki pages compiled from their notes, sources, and decisions. Every agent can read all of it. It is read-only.

## Setup

Load these from the process environment, or from `.env` in this skill folder if a variable is unset:
- `VAULT_MCP_URL`: the MCP endpoint.
- `VAULT_AGENT_NAME`: your agent's name.

If `VAULT_MCP_URL` is missing, stop and tell the user.

## Connect

1. If `vault` tools (`search`, `read_note`, `list_notes`, `list_projects`) are already in your tool list, use them and skip the rest of this section.
2. If your harness takes remote MCP servers, add the server once with the agent-name header, then use its tools. For example, in Claude Code:

   ```sh
   claude mcp add --transport http vault "$VAULT_MCP_URL" --header "X-Vault-Agent-Name: $VAULT_AGENT_NAME"
   ```

3. Otherwise call it with `curl` and `jq`. The server is stateless: each tool call is one POST with one JSON reply. Load `.env` with `set -a; . <skill-folder>/.env; set +a`, then define this once per shell:

   ```sh
   vault() {
     local args=${2:-'{}'}
     curl -fsS "$VAULT_MCP_URL" \
       -H 'Content-Type: application/json' -H 'Accept: application/json' \
       -H "X-Vault-Agent-Name: $VAULT_AGENT_NAME" \
       -d "$(jq -nc --arg t "$1" --argjson a "$args" \
         '{jsonrpc: "2.0", id: 1, method: "tools/call", params: {name: $t, arguments: $a}}')" \
       | jq -r '.result.content[0].text // .error // .'
   }

   vault search '{"query": "rails connection pool", "limit": 5}'
   vault read_note '{"path": "wiki/concepts/example.md", "section": "Scoring"}'
   vault list_notes '{"project": "rails-performance", "tags": "puma,memory"}'
   vault list_projects
   ```

The server is reachable only from devices on the user's tailnet. If the connection fails or times out, tell the user. Don't look for another route.

## Tools

| tool | use |
|---|---|
| `search` | Find pages. `query`, optional `project`, `tags` (comma-separated), `type`, `limit` (default 8, max 20), `after`. |
| `read_note` | Read one page by `path`, optionally one `section`. Long pages without `section` return a heading outline. |
| `list_notes` | Browse pages by `project`, `tags`, or `type`. `limit` default 20, max 100. Page with `after` set to the last path. |
| `list_projects` | List every project with a one-line description. |

## Use

1. `search` with the key terms. Search is keyword-only, so use the words a note would contain, not a question.
2. With zero hits, retry with fewer words, synonyms, or the product or person name. Then try `list_projects` and `list_notes` for the likely project.
3. `read_note` the best hits before you rely on them. Snippets are not enough.
4. Cite the page path for every fact you take from the vault. Pages cite their own sources; follow those when you need more detail.

Results mask anything that looks like a secret. Don't try to recover masked values.

