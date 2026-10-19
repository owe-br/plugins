# gmaps.dev

Find businesses by what they are and where they are, such as bakeries in Curitiba or dentists
near a point. The plugin connects your agent to [gmaps.dev](https://gmaps.dev/en) and teaches it
how to use the tools: search an area, collect a whole city, and hand you the list as a csv, json
or xlsx file. gmaps.dev is not affiliated with Google.

## What's inside

- A skill for choosing the area, checking the cost first, following a collection and exporting
  the places.
- The remote MCP server at `https://api.gmaps.dev/mcp`. Nothing runs on your machine.
- Manifests for Claude Code and Agent Plugins (ChatGPT, Codex and Cursor).

The server has 18 tools. Places gmaps.dev already saved come back for free. Each new place costs one
credit. Looking for emails needs a paid plan and costs one more credit for each place where one is
found. Only `search_places` and `create_collection` can spend credits. The skill gets a free quote
before it starts a large collection.

## Install

In Claude Code:

```sh
claude plugin marketplace add owe-br/plugins
claude plugin install gmaps@owe-br
```

In Codex:

```sh
codex plugin marketplace add owe-br/plugins
codex plugin add gmaps@owe-br
```

## Sign in

In Claude Code, type `/mcp`, choose gmaps and Authenticate. In Codex 0.147 or later, run
`codex mcp login gmaps`. The browser opens console.gmaps.dev. Sign in, check the app's name and
return address, and press Connect.

The app gets its own API key. It appears under [API keys](https://console.gmaps.dev/keys), named
after the app, and counts toward your plan's key limit. Its calls use your credits like any other
key's. Revoke it there to disconnect. No key needs to be pasted into this plugin's files.

On a machine with no browser, the skill uses a device code with `client_id=gmaps-agent`. Open
the link on another device, check the code and approve it. The code expires in 10 minutes.

## Links

- [MCP tools and setup](https://gmaps.dev/docs/en/mcp)
- [Privacy for connected apps](https://gmaps.dev/en/privacy#ai-apps)
- [Terms](https://gmaps.dev/en/terms)
- [Acceptable use policy](https://gmaps.dev/en/aup)
- Help: [hello@gmaps.dev](mailto:hello@gmaps.dev)
- Privacy questions: [privacy@gmaps.dev](mailto:privacy@gmaps.dev)
