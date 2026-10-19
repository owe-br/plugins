# SmartGenius

SmartGenius is a social media manager for Instagram. This plugin lets your agent use it: ask
for a post, a carousel or a story for one of your profiles, and SmartGenius plans the slides,
writes the text and the caption, and draws each image in that profile's voice and visual style.
It can also draw an image from any prompt.

Every post lands as a draft. You approve, schedule or publish it yourself in the SmartGenius
studio; the agent can't.

## What's inside

- The SmartGenius MCP server at `https://api.smartgenius.app/mcp`. Its tools act as you, with
  your role in the workspace.
- A skill that teaches the agent the workflows: pick a profile, make a post and wait for it, draw
  images, and read each error before retrying.

## Install

In Claude Code:

```sh
claude plugin marketplace add owe-br/plugins
claude plugin install smartgenius@owe-br
```

In Codex:

```sh
codex plugin marketplace add owe-br/plugins
codex plugin add smartgenius@owe-br
```

## Sign in

In Claude Code, type `/mcp`, pick smartgenius and choose Authenticate. In Codex, run
`codex mcp login smartgenius` (Codex 0.147 or later; update with
`npm install -g @openai/codex@latest`).

Your browser opens SmartGenius: check the app's name and the address it sends you back to, then
press Allow. That makes an API key named after the app. A workspace admin sees it under API and
MCP in the workspace menu and can revoke it there at any time.

Only an admin of the workspace can connect an app to it. Anyone else is asked to have an admin do
it.

No browser on the machine? The skill shows the agent how to sign in with a short code. Open the
link it gives you on any device, check that the code matches, pick the workspace and press Allow.
The agent gets a key named "AI agent (device sign-in)", listed under API and MCP. You can also
make a key there yourself and give it to your agent.

## Images and limits

Every image comes out of the workspace's monthly quota: one per slide of a post, and one per
generated image. A failed image doesn't count. Download links for generated images last 7 days.

## Links

- Setup guide and tool list: https://smartgenius.app/en/docs
- What to try, and what should be refused: [TESTING.md](TESTING.md)
- Privacy when you connect an AI app: https://smartgenius.app/en/privacidade/apps-de-ia
- Privacy policy: https://smartgenius.app/en/privacidade
- Terms: https://smartgenius.app/en/termos
- Help: info@olhary.ai
