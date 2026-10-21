# voar

Read your organization's GitHub Actions jobs and usage on [voar](https://voar.dev/en) from your
agent. voar runs GitHub Actions jobs on machines in São Paulo, Brazil. The plugin connects your
agent to voar and teaches it how to read the answers: the organization's status, its recent jobs
with the machine size and the reason a job did not start, and a month's usage day by day. voar is
not affiliated with GitHub.

## What's inside

- A skill for reading the three tools, turning micros into money, explaining why a job did not
  start and handling errors.
- The remote MCP server at `https://api.voar.dev/mcp`. Nothing runs on your machine.
- Manifests for Claude Code and Agent Plugins (ChatGPT, Codex and Cursor).

The server has 3 tools, all read-only: `get_account`, `list_jobs` and `get_usage`. None can start
or cancel a job, add credit, change a limit or create a key.

## Install

In Claude Code:

```sh
claude plugin marketplace add owe-br/plugins
claude plugin install voar@owe-br
```

In Codex:

```sh
codex plugin marketplace add owe-br/plugins
codex plugin add voar@owe-br
```

## Sign in

In Claude Code, type `/mcp`, choose voar and Authenticate. In Codex 0.147 or later, run
`codex mcp login voar`. The browser opens app.voar.dev. Sign in with GitHub, pick the organization,
check the app's name and return address, and press Connect organization.

Only owners and admins of the organization can connect an app. The app gets its own read-only API
key, which starts with `voar_`. It appears in the API keys section of the organization's Settings
at [app.voar.dev](https://app.voar.dev) and counts toward the limit of 10 active keys. Revoke it
there to disconnect. No key needs to be pasted into this plugin's files.

On a machine with no browser, the skill uses a device code with `client_id=voar-agent`. Open the
link on another device, check the 8-letter code and approve it. The code expires in 10 minutes.

## Links

- [API and MCP guide](https://voar.dev/en/docs#api)
- [Privacy for connected AI apps](https://voar.dev/en/docs#ai-apps)
- Help: [contato@voar.dev](mailto:contato@voar.dev)
