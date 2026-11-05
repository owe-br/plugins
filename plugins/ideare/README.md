# ideare

ideare makes a small business's brand kit: the logo in every version, colors and fonts, site
icons, share cards, every social size, an email signature, a business card and guidelines in
plain words. This plugin lets your agent use it: read an approved brand and the link to each
file, put the brand in a codebase, change the brand's draft and check it, and draw AI symbols and
art in the brand's style.

Nothing goes public until an owner approves it. When your agent asks to approve a change, the
owner gets a proposal and approves it in one tap in the ideare studio.

## What's inside

- The ideare MCP server at `https://api.ideare.app/mcp`. Its tools act as you, with your role in
  the workspace.
- A skill that teaches the agent the workflows: read a brand and its files, run
  `npx ideare init` in a project, change and check the draft, ask for approval, draw symbols and
  art, and read each error before retrying.

## Install

In Claude Code:

```sh
claude plugin marketplace add owe-br/plugins
claude plugin install ideare@owe-br
```

In Codex:

```sh
codex plugin marketplace add owe-br/plugins
codex plugin add ideare@owe-br
```

## Sign in

In Claude Code, type `/mcp`, pick ideare and choose Authenticate. In Codex, run
`codex mcp login ideare`.

Your browser opens ideare: check the app's name and the address it sends you back to, then press
Allow. That makes an API key named after the app. You see it in the studio, under Keys, and can
revoke it there at any time. A key made this way never publishes: its approvals become proposals.

You can also make a key in the studio, under Keys, and give it to your agent. On the free plan,
keys can only read.

## Credits

Reading, saving, checking and approving are free. Only AI pictures cost credits: 1 per symbol
idea, and 1 per art picture at 1k or 2 at 2k. A picture that fails gives its credit back.

## Links

- ideare: https://ideare.app/en
- Privacy when you connect an AI app: https://ideare.app/en/privacy/ai-apps
- Help: hello@ideare.app
