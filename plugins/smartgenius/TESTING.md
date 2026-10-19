# Testing the SmartGenius plugin

How to try every part of this plugin, written for store reviewers and anyone else.

## The test account

Store reviewers get an email and password in the submission form. It signs in with no second step.

The account owns one Espaço (workspace), "SmartGenius", with one Instagram profile,
@smartgenius.app. SmartGenius read that profile's public page to learn its voice and colors. No
Instagram account is connected, so nothing can be published from it. The Espaço already holds one
draft carousel, "Plan a Week in 15 Minutes". It can make 100 images a month, at most 30 a day.
The account can't see any other Espaço.

## Sign in

1. Install the plugin (see [README.md](README.md)).
2. Claude Code: type `/mcp`, pick smartgenius, choose Authenticate. Codex: run
   `codex mcp login smartgenius` (Codex 0.147 or later). ChatGPT: add the connector, then press
   Connect.
3. SmartGenius opens in your browser. Sign in with the test account, check the app's name and the
   address it returns to, and press Allow.

To disconnect, revoke the key named after the app under API and MCP in the workspace menu on
my.smartgenius.app.

### With no browser

An agent on a server or over SSH signs in with a short code instead:

1. Ask the agent to connect to SmartGenius. It shows a link and a code like `WDJB-MJHT`.
2. Open the link on any device, or go to https://my.smartgenius.app/device and type the code.
3. Sign in with the test account, check that the code matches, pick the "SmartGenius" Espaço and
   press Allow. The code lasts 10 minutes.

The agent gets a key named "AI agent (device sign-in)", listed under API and MCP. Revoke it there
to disconnect.

## Should work

| Ask                                                                                          | What happens                                                                                                                                              |
| -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Which Instagram profiles can I make posts for?"                                             | Lists one profile, @smartgenius.app, with its studio link.                                                                                                |
| "How many images do I have left this month?"                                                 | Says how many of the 100 monthly images are left, how many of today's 30, and when the count resets (the 1st of the month).                               |
| "Make a 3-slide carousel for @smartgenius.app about planning a week of posts in 15 minutes." | Starts the post, then waits for it (a few minutes). Shows each slide's text, the caption, the hashtags and the studio link. It is a draft. Uses 3 images. |
| "Draw a photo of a sunlit bakery counter with fresh sourdough loaves."                       | Draws one 1024×1024 image from the prompt as written and returns its link, which works for 7 days. Uses 1 image.                                          |
| "Draw a 4:5 image for @smartgenius.app that announces a new feature."                        | Draws one image in the profile's look (its colors and visual style) and returns its link. Uses 1 image.                                                   |

## Should not work

| Ask                                              | What happens                                                                                                            |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| "Publish the carousel to Instagram now."         | No tool publishes or schedules. The agent says the post is a draft and a person approves it in the studio, at its link. |
| "Make a carousel for @nike about running shoes." | SmartGenius answers "Profile @nike not found". No images are used. The agent lists the profile the account has.         |
| "What's the weather in Lisbon tomorrow?"         | No SmartGenius tool is called.                                                                                          |

## What each tool can change

Every tool says whether it only reads or adds data, through `readOnlyHint`, `destructiveHint` and
`openWorldHint`. `list_profiles`, `get_post` and `get_usage` only read. `create_post` and
`generate_image` add a draft or an image and use images from the monthly count. No tool edits,
deletes or publishes anything. Tools act as the signed-in person, with that person's role in the
Espaço. A tool can't do anything that person couldn't do in the app.
