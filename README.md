# owe-br plugins

Plugins for owe-br's products. Each one connects your agent to a product's MCP server and
teaches it that product's workflows with a skill.

| Plugin                     | What it does                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------ |
| [featury](plugins/featury) | Triage your product's requests, see what shipped and what's being built, and run its public changelog. |

## Install

In Claude Code:

```sh
claude plugin marketplace add owe-br/plugins
claude plugin install featury@owe-br
```

In Codex:

```sh
codex plugin marketplace add owe-br/plugins
codex plugin add featury@owe-br
```

Each plugin's README says how to sign in.

## Layout

- `.claude-plugin/marketplace.json` lists the plugins. Claude Code and Codex both read it.
- `plugins/<name>/` holds one plugin: its skills, its MCP server address in `.mcp.json` (Claude)
  and `mcp.json` (Agent Plugins, read by ChatGPT, Codex and Cursor), and a manifest for each
  format.
- `registry/<name>/server.json` lists the plugin's MCP server in the
  [MCP Registry](https://registry.modelcontextprotocol.io).

Every push checks the Claude files with `claude plugin validate --strict`, the Agent Plugins files
against the spec's schemas, and each registry entry with `mcp-publisher validate`.
