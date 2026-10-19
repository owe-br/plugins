# scrapa.app

Read web pages as markdown, search the web, list a site's URLs and run a real Chrome. The plugin
connects your agent to [scrapa.app](https://scrapa.app/en) and teaches it how to use the tools.
scrapa reads each page with a plain HTTP request or a real browser, whichever the page needs, and
every request leaves through a residential proxy or your own.

## What's inside

- A skill for picking the right tool, keeping costs down, reading a refusal before retrying, and
  following a batch or a browser session.
- The remote MCP server at `https://api.scrapa.app/mcp`. Nothing runs on your machine.
- Manifests for Claude Code and Agent Plugins (ChatGPT, Codex and Cursor).

The server has 16 tools. Every answer says what it cost and how many credits are left. A page
the site blocked and a URL scrapa refused cost nothing, unless a script you sent ran in the page
first. A failure on scrapa's side is always free. Reading a page, mapping a site, a batch and a
browser session each have a free tool that says the price first.

## Install

In Claude Code:

```sh
claude plugin marketplace add owe-br/plugins
claude plugin install scrapa@owe-br
```

In Codex:

```sh
codex plugin marketplace add owe-br/plugins
codex plugin add scrapa@owe-br
```

## Sign in

In Claude Code, type `/mcp`, choose scrapa and Authenticate. In Codex 0.147 or later, run
`codex mcp login scrapa`. The browser opens console.scrapa.app. Sign in, check the app's name and
return address, and approve the connection.

The app gets its own API key on your account. It appears on the
[Keys page](https://console.scrapa.app/keys) and counts toward your plan's key limit. Its calls
use your credits like any other key's. Revoke it there to disconnect. No key needs to be pasted
into this plugin's files.

On a machine with no browser, the skill uses a device code with `client_id=scrapa-agent`. Open
the link on another device, check the code and approve it. The code expires in 10 minutes.

To make the tools read from one place by default, add it to the server address, such as
`https://api.scrapa.app/mcp?country=br&city=curitiba`.

## Links

- [MCP setup](https://docs.scrapa.app/en/mcp)
- [Privacy](https://scrapa.app/en/privacy)
- [Terms](https://scrapa.app/en/terms)
- [Acceptable use policy](https://scrapa.app/en/aup)
- Help: [hello@scrapa.app](mailto:hello@scrapa.app)
- Privacy questions: [privacy@scrapa.app](mailto:privacy@scrapa.app)
