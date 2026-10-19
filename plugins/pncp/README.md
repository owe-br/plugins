# pncp.dev

Query PNCP, Brazil's national public procurement portal, from your agent: tenders published in a
period, tenders still open for proposals, signed contracts, price records (atas de registro de
preço) and one purchase in detail. The plugin connects your agent to [pncp.dev](https://pncp.dev)
and teaches it how to use the tools. pncp.dev serves PNCP's public API under the same routes and
filters. The site and the data are in Portuguese. pncp.dev is not affiliated with PNCP, the
Brazilian government or Cloudflare.

## What's inside

- A skill for building the PNCP route, reading the answer, keeping the number of pages small and
  stopping on a refusal.
- The remote MCP server at `https://api.pncp.dev/mcp`. Nothing runs on your machine.
- Manifests for Claude Code and Agent Plugins (ChatGPT, Codex and Cursor).

The server has 2 tools, both read-only. `get_pncp` reads one page of a PNCP `/api/` route and uses
one request of your monthly quota, even when the answer comes from the cache. A refused call counts
too. `get_usage` shows this month's usage, quota and credits, and is free.

## Install

In Claude Code:

```sh
claude plugin marketplace add owe-br/plugins
claude plugin install pncp@owe-br
```

In Codex:

```sh
codex plugin marketplace add owe-br/plugins
codex plugin add pncp@owe-br
```

## Sign in

In Claude Code, type `/mcp`, choose pncp and Authenticate. In Codex 0.147 or later, run
`codex mcp login pncp`. The browser opens pncp.dev. Sign in, check the app's name and return
address, and press Conectar.

The app gets its own API key, named after the app. It appears under
[Chaves](https://pncp.dev/app/chaves) and counts toward the limit of 10 active keys. Its calls use
your quota like any other key's. Revoke it there to disconnect; calls it made before still count
toward the month. No key needs to be pasted into this plugin's files.

On a machine with no browser, the skill uses a device code with `client_id=pncp-cli`. Open the link
on another device, check the 8-letter code and approve it. The code expires in 10 minutes.

## Links

- [MCP setup, in Portuguese](https://pncp.dev/docs#mcp)
- [Privacy for AI apps](https://pncp.dev/privacidade#apps-de-ia)
- [Terms](https://pncp.dev/termos)
- Help: [suporte@pncp.dev](mailto:suporte@pncp.dev)
