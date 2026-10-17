# socially.run

Read public social profiles and posts, search topics and usernames, and follow lookup jobs.
The plugin connects your agent to [socially.run](https://socially.run) and teaches it how to use
the tools. It cannot sign into social accounts or read private messages.

## What's inside

- A skill for choosing a tool, reading its result and following a background job.
- The remote MCP server at `https://api.socially.run/mcp`. Nothing runs on your machine.
- Manifests for Claude Code and Agent Plugins (ChatGPT, Codex and Cursor).

The server has 25 tools. Some read public pages and spend credits. Others start a background
search, cancel a job or change your webhook. The skill explains those differences and asks
before starting a search that builds a report about a person.

## Install

In Claude Code:

```sh
claude plugin marketplace add owe-br/plugins
claude plugin install socially@owe-br
```

In Codex:

```sh
codex plugin marketplace add owe-br/plugins
codex plugin add socially@owe-br
```

## Sign in

In Claude Code, type `/mcp`, choose socially and Authenticate. In Codex 0.147 or later, run
`codex mcp login socially`. The browser opens console.socially.run. Sign in, check the app's name
and return address, and approve the connection.

The app gets its own API key. It appears under [API keys](https://console.socially.run/keys),
named after the app, and uses one of your plan's key slots. Revoke it there to disconnect.
No key needs to be pasted into this plugin's files.

On a machine with no browser, the skill uses a device code with `client_id=socially-agent`.
Open the link on another device, check the code and approve it. The code expires in 10 minutes.

## Links

- [MCP tools and setup](https://socially.run/docs/en/mcp)
- [Privacy for connected apps](https://socially.run/en/privacy#ai-apps)
- [Terms](https://socially.run/en/terms)
- Help: [hello@socially.run](mailto:hello@socially.run)
- Privacy questions: [privacy@socially.run](mailto:privacy@socially.run)
