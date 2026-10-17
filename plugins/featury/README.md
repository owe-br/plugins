# featury

featury reads your code and keeps a map of what your product does, what shipped and what is
being built. This plugin lets your agent work with it: triage the requests your team and
customers send, file new ones, answer "does it already do X?", and run the product's public
changelog.

## What's inside

- The featury MCP server at `https://api.featury.app/mcp`. Its tools act as you, with your
  permissions in each organization you belong to.
- A skill that teaches the agent featury's workflows: triage, grooming the board, closing the
  loop from a commit, and the changelog.

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

## Sign in

In Claude Code, type `/mcp`, pick featury and choose Authenticate. In Codex, run
`codex mcp login featury`.

Your browser opens featury: check the app's name and the address it sends you back to, then press
Connect. That makes an API key named after the app. It is listed under Account → API keys, where
you can revoke it at any time.

No browser on the machine? The skill shows the agent how to sign in with a short code that you
approve from any device where you are signed in to featury.

## Links

- Setup guide and tool list: https://featury.app/en/docs/mcp
- Privacy when you connect an AI app: https://featury.app/en/privacy/ai-apps
- Terms: https://featury.app/en/terms
- Help: gustavo@openwings.com.br
