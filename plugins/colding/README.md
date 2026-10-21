# colding

Read and answer email, manage contacts and campaigns, check addresses and send app mail through
your workspace's mailboxes. The plugin connects your agent to [colding](https://colding.app/en) and
teaches it how to use the tools safely.

## What's inside

- A skill for reading and organizing threads, writing drafts and replies, checking addresses,
  managing contacts and campaigns, sending app mail, opening handoffs when a human action is
  required, and handling refusals and idempotency keys.
- The remote MCP server at `https://api.colding.app/mcp`. Nothing runs on your machine.
- Manifests for Claude Code and Agent Plugins (ChatGPT, Codex and Cursor).

Each connection belongs to one workspace and shows only the tools its permissions and mailbox read
list allow (64 tools with `read` alone, 75 when limited to a mailbox read list across all six key
permissions, and up to 148 across all six key permissions without a read list). Protected owner
actions, such as connecting a mailbox or managing keys and webhooks, never run on a key.

## Install

In Claude Code:

```sh
claude plugin marketplace add owe-br/plugins
claude plugin install colding@owe-br
```

In Codex:

```sh
codex plugin marketplace add owe-br/plugins
codex plugin add colding@owe-br
```

## Sign in

In Claude Code, type `/mcp`, choose colding and Authenticate. In Codex 0.147 or later, run
`codex mcp login colding`. The browser opens `https://console.colding.app/auth/authorize`. Sign in
to your existing colding account, pick a workspace you own, check the app's name and return
address, choose the permissions and optional limits (`Read` is selected to start), and press
Connect. Accounts are opened by hand while public signup stays closed.

The app gets its own `cd_` API key in that workspace. It appears in Settings, then API keys at
[console.colding.app](https://console.colding.app), where the workspace owner can change its limits
or revoke it at any time. No key needs to be pasted into this plugin's files.

On a machine with no browser, the skill uses a device code with `client_id=colding-cli`. Open
`https://console.colding.app/auth/device` on another device, check the code and approve it. The
code expires in 10 minutes.

## Links

- [Documentation and MCP guide](https://colding.app/en/docs)
- [Privacy](https://colding.app/en/privacy)
- [Terms](https://colding.app/en/terms)
- [Acceptable use policy](https://colding.app/en/aup)
- Help: [hello@colding.app](mailto:hello@colding.app)
- Privacy questions: [privacy@colding.app](mailto:privacy@colding.app)
