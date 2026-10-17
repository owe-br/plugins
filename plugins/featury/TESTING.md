# Testing the featury plugin

How to try every part of this plugin, written for store reviewers and anyone else.

## The test account

Store reviewers get an email and password in the submission form. It signs in with no second step.

The account owns one organization, "featury demo", with one product, "falai agent". featury mapped
it from [falai-dev/agent](https://github.com/falai-dev/agent), a public open-source repo. It also
holds 7 sample requests (one merged into another, one planned, one closed) and one recorded
decision. The account can't see any other organization.

## Sign in

1. Install the plugin (see [README.md](README.md)).
2. Claude Code: type `/mcp`, pick featury, choose Authenticate. Codex: `codex mcp login featury`
   (Codex 0.147 or later). ChatGPT and claude.ai: add the connector, then press Connect.
3. featury opens in your browser. Sign in with the test account, check the app's name and the
   address it returns to, and press Connect.

To disconnect, revoke the key named after the app under Account → API keys on my.featury.app.

## Should work

| Ask                                                                                     | What happens                                                                                                                                   |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| "What does falai agent do?"                                                             | Reads the product's areas and features, then describes them: conversation flows, the turn engine, model connections, memory, tools and guides. |
| "Which requests are open in falai agent?"                                               | Lists 5 requests: streaming replies, two bugs, token counts, and Mistral as planned. Closed and merged requests are left out.                  |
| "File a bug in falai agent: GeminiProvider times out after 30 seconds on long prompts." | Creates a bug and returns its reference code. It then shows up in the list.                                                                    |
| "Mark the wait-step bug as planned, with a note that the fix ships next week."          | Changes that request to planned. The note goes on its timeline.                                                                                |
| "What changed in falai agent recently?"                                                 | Lists the latest changes found in the repo's commits, each with a short summary.                                                               |
| "Draft the next changelog for falai agent."                                             | Builds a draft edition from the changes not yet published. Nothing goes public until a person publishes it.                                    |

## Should not work

| Ask                                              | What happens                                                                     |
| ------------------------------------------------ | -------------------------------------------------------------------------------- |
| "What's the weather in Lisbon tomorrow?"         | No featury tool is called.                                                       |
| "Show me the requests in the acme organization." | featury answers "Workspace not found". The agent says the account has no access. |
| "Delete the falai agent product."                | No tool deletes a product. The agent says this can only be done in the app.      |

## What each tool can change

Every tool says whether it only reads, adds, or changes data, through `readOnlyHint`,
`destructiveHint` and `openWorldHint`. Tools act as the signed-in person, with that person's role
in each organization. A tool can't do anything that person couldn't do in the app.
