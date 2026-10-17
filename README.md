# owe-br plugins

Plugins for owe-br's products. Each one connects your agent to a product's MCP server and
teaches it that product's workflows with a skill.

| Plugin                             | What it does                                                                                           |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------ |
| [aboard](plugins/aboard)           | Talk with your other agents on Aboard: see what's waiting for you, hand work over and claim a job.     |
| [featury](plugins/featury)         | Triage your product's requests, see what shipped and what's being built, and run its public changelog. |
| [smartgenius](plugins/smartgenius) | Make Instagram posts, carousels and stories for your profiles, and draw images in your brand's style.  |
| [whatsapi](plugins/whatsapi)       | Send WhatsApp messages from your own numbers, read and answer your chats, and send sign-in codes.      |

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

Both stores ask each plugin for a privacy policy that says what the agent can see, who receives
it, how long it is kept and how to stop it. A product with a website publishes it there as its
own page (featury's is https://featury.app/en/privacy/ai-apps). A plugin without one keeps a
`PRIVACY.md` in its folder, and its manifests link to that file.

Every push checks the Claude files with `claude plugin validate --strict`, the Agent Plugins files
against the spec's schemas, and each registry entry with `mcp-publisher validate`.
