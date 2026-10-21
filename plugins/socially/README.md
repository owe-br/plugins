# socially.run

Read public social profiles and posts, read web pages, and search videos, news and trends from
your agent. The plugin connects your agent to [socially.run](https://socially.run) and teaches it
how to use the tools. It does not sign in to social accounts or read private messages.

## What's inside

- A skill for choosing a tool, reading its answer honestly and stopping on a refusal.
- The remote MCP server at `https://api.socially.run/mcp/store`. Nothing runs on your machine.
- Manifests for Claude Code and Agent Plugins (ChatGPT, Codex and Cursor).

The server has 11 tools, all read-only. Four read one public thing at a time: a profile, a post, a
web page and a page's link preview. Four look for what is being published or is trending: videos
on YouTube, news on Google News, popular reels on Instagram's public topic pages and a country's
trend board. Three describe the service: what a link points to, which platforms work right now and
which projects socially builds on.

Some reads go through a paid data provider's API instead of the page itself. A profile or post
that socially cannot check comes back as "could not check", never as "not found".

It cannot find a person's accounts on other sites, look anyone up by email or username, or start a
background search. Those stay on the full API, which you reach with your own key.

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
named after the app. Like any key, it can do what your other keys can, even though this server
lists only read tools. Revoke it there to disconnect. No key needs to be pasted into this plugin's
files.

On a machine with no browser, the skill uses a device code with `client_id=socially-agent`.
Open the link on another device, check the code and approve it. The code expires in 10 minutes.

## Links

- [MCP tools and setup](https://socially.run/docs/en/mcp)
- [Privacy for connected apps](https://socially.run/en/privacy#ai-apps)
- What to try, and what should be refused: [TESTING.md](TESTING.md)
- [Terms](https://socially.run/en/terms)
- Help: [hello@socially.run](mailto:hello@socially.run)
- Privacy questions: [privacy@socially.run](mailto:privacy@socially.run)
