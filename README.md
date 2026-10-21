# owe-br plugins

Plugins for owe-br's products. Each one connects your agent to a product's MCP server and
teaches it that product's workflows with a skill.

| Plugin                             | What it does                                                                                           |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------ |
| [aboard](plugins/aboard)           | Talk with your other agents on Aboard: see what's waiting for you, hand work over and claim a job.     |
| [featury](plugins/featury)         | Triage your product's requests, see what shipped and what's being built, and run its public changelog. |
| [smartgenius](plugins/smartgenius) | Make Instagram posts, carousels and stories for your profiles, and draw images in your brand's style.  |
| [whatsapi](plugins/whatsapi)       | Send WhatsApp messages from your own numbers, read and answer your chats, and send sign-in codes.      |
| [socially](plugins/socially)       | Read public social profiles and posts, search topics and usernames, and follow lookup jobs.            |
| [gmaps](plugins/gmaps)             | Find businesses by what they are and where they are, collect a whole city, and export the list.        |
| [scrapa](plugins/scrapa)           | Read web pages as markdown, search the web, list a site's URLs and run a real Chrome.                  |
| [pncp](plugins/pncp)               | Query Brazil's public procurement portal (PNCP): tenders, contracts and price records.                 |
| [voar](plugins/voar)               | Read your organization's GitHub Actions jobs and usage on voar. Read-only.                             |

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

## Build an OpenAI upload

```sh
python3 scripts/export-openai.py featury
```

This writes `dist/featury-openai-plugin.zip`. Use another plugin name to build its ZIP, or
`--output <path>` to choose where it goes. The exporter reads the committed plugin files at `HEAD`,
not uncommitted edits. Commit plugin changes before exporting. It never copies untracked files,
environment files or key files.

All current plugins use OAuth remote servers. The ZIP adds OpenAI's
[documented authentication settings](https://developers.openai.com/plugins/build/plugins#configure-mcp-authentication)
to each server: `extensions["com.openai"].auth` selects `oauth` with `client.mode: "cimd"`.
CIMD lets the client identify itself with a metadata document; dynamic client registration stays
available as a fallback. The server supplies the OAuth endpoints through discovery. No client
secret, API key or access token belongs in the ZIP.

The source `mcp.json` stays valid against the published Agent Plugins 1.0 schema. That schema
rejects OpenAI's per-server `extensions` field, so the generated upload is OpenAI-specific, not a
portable MCP config. It keeps the `$schema` marker shown in OpenAI's example. CI checks the upload's
transport fields against the unchanged portable schema and its auth fields against our closed,
docs-derived OAuth profile in `schemas/openai-oauth.schema.json`. This profile checks the settings
we export; it is not an official OpenAI schema or a list of every auth method OpenAI supports.
Local servers and fixed-key configs are not supported by this exporter.

Run the local export check after changing the exporter:

```sh
python3 scripts/check-openai-export.py
```

It checks every plugin's ZIP, unchanged source files, repeatable output and rejected credentials
or unsupported auth settings. It does not run in CI.

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
against the spec's schemas, OpenAI upload packages as described above, and each registry entry with
`mcp-publisher validate`.
