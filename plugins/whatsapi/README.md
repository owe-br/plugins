# whatsapi.sh

whatsapi.sh links your own WhatsApp numbers the way WhatsApp Web does: the phone keeps working,
and your agent can use the number too. This plugin lets it read and answer your chats, send
messages, photos, files and locations, send and check sign-in codes, and pair a new number.

whatsapi.sh is not the official WhatsApp Business API. WhatsApp can restrict a number that sends
like a machine, so messages to people who haven't written to you in the last 24 hours wait in a
queue and leave 15 to 25 minutes apart.

## What's inside

- The whatsapi.sh MCP server at `https://api.whatsapi.sh/mcp`. Its tools act as you, on the
  numbers in your account.
- A skill that teaches the agent the workflows: check the number first, send safely with the
  queue, read and answer a chat, sign-in codes, and pairing a number.

## Install

In Claude Code:

```sh
claude plugin marketplace add owe-br/plugins
claude plugin install whatsapi@owe-br
```

In Codex:

```sh
codex plugin marketplace add owe-br/plugins
codex plugin add whatsapi@owe-br
```

## Sign in

In Claude Code, type `/mcp`, pick whatsapi and choose Authenticate. In Codex, run
`codex mcp login whatsapi`. This needs Codex 0.147 or later: older versions stop with "missing
required issuer". Update with `npm install -g @openai/codex@latest`, then sign in again.

Your browser opens whatsapi.sh: sign in, check the app's name and the address it sends you back
to, then press Connect. That makes an API key named after the app. It is listed under API keys in
the dashboard, where you can revoke it at any time. Its messages count toward your monthly quota
like any other key's.

No browser on the machine? The skill shows the agent how to sign in with a short code that you
approve from any device where you are signed in to whatsapi.sh.

## Links

- Setup guide and tool list: https://docs.whatsapi.sh/en/mcp
- Avoiding bans: https://docs.whatsapi.sh/en/guides/bans
- Privacy when you connect an AI app: https://whatsapi.sh/en/privacy/ai-apps
- Terms: https://whatsapi.sh/en/terms
- Help: gustavo@openwings.com.br
