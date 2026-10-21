# Testing the socially.run plugin

How to try every part of this plugin, written for store reviewers and anyone else.

## The test account

Store reviewers get an email and password in the submission form. Use them to sign in.

## Sign in

1. Install the plugin (see [README.md](README.md)).
2. Claude Code: type `/mcp`, pick socially, choose Authenticate. Codex: `codex mcp login socially`
   (Codex 0.147 or later). ChatGPT and claude.ai: add the connector, then press Connect.
3. console.socially.run opens in your browser. Sign in with the test account.
4. The next page shows the app's name and the address it returns to. Check them, then press
   Connect.

The app gets its own API key, named after the app. To disconnect, revoke that key under
[API keys](https://console.socially.run/keys).

## Should work

Live pages change, so answers are described by their shape, not their numbers.

| Ask                                                                                 | What happens                                                                                                                                                                              |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "What does https://www.instagram.com/nasa/ point to?"                               | Calls `resolve_target`. Answers platform `instagram`, kind `profile`, handle `nasa` and the canonical link. Nothing is fetched.                                                           |
| "Read the public Instagram profile https://www.instagram.com/nasa/."                | Calls `lookup_profile`. Answers `found` with the name, bio, public counts and recent posts, or `undecided` when Instagram blocks the read. The agent never calls `undecided` "not found". |
| "What is trending in Brazil right now?"                                             | Calls `list_trending` with `geo` BR. Shows rising searches with the news behind each. If the source refuses, the last saved board comes back marked `stale` with its capture time.        |
| "What news was published about urban gardening this week?"                          | Calls `search_news` with `q` and `recency` week. Shows headlines, publishers and dates.                                                                                                   |
| "Find YouTube videos about urban gardening from the last month, most viewed first." | Calls `search_youtube` with `recency` month and `sort` views. Shows titles, channels, view counts and durations.                                                                          |
| "Summarize https://socially.run."                                                   | Calls `read_website`. Shows the page's title and readable text.                                                                                                                           |
| "Which platforms does socially read, and which work right now?"                     | Calls `list_platforms`. Shows what each platform supports and the health of each source.                                                                                                  |

## Should not work

| Ask                                                       | What happens                                                                                   |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| "Find every account that uses the handle nasa."           | No tool searches by username. The agent says so and does not try guessed handles one by one.   |
| "Which accounts are registered with someone@example.com?" | No tool takes an email address. The agent says it cannot do that here.                         |
| "Read the direct messages of my Instagram account."       | socially never signs in to social accounts, so there is nothing to read. The agent declines.   |
| "Read http://127.0.0.1:8080/admin with socially."         | `read_website` refuses private and internal addresses with `SSRF_BLOCKED`. Nothing is fetched. |
| "Register a webhook for my socially account."             | No tool does it. The server lists only read tools.                                             |

## What each tool can change

Every tool says what it does through `readOnlyHint`, `destructiveHint` and `openWorldHint`. All 11
are read-only: `readOnlyHint` is true and `destructiveHint` is false.

- `resolve_target`, `list_platforms` and `get_attributions` reach nothing outside socially, so
  `openWorldHint` is false.
- `lookup_profile`, `lookup_post`, `read_website`, `fetch_og`, `list_trending`, `search_youtube`,
  `search_news` and `search_instagram` read public pages and feeds on the open web, so
  `openWorldHint` is true. They post, send and delete nothing anywhere.

Each call is recorded in the signed-in account's usage history. No tool can change the account,
its keys or its settings. Only a person signed in at console.socially.run can.
