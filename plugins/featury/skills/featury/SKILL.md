---
name: featury
description: "Work with featury (the team's engineering-visibility system) over its MCP tools. Use when the user asks about featury requests (bugs/feature asks), wants to triage or act on them, asks what exists in a project, what shipped, or what's being built right now, wants to run the product's public changelog (its notes, rhythm, draft edition or publishing), or wants to consult featury's codebase agent. Requires the featury MCP server to be configured (setup guide: https://featury.app/en/docs/mcp)."
---

# featury workflows

featury tracks **requests** (agent-triaged bug reports + feature asks), a living **feature
inventory**, **classified changes**, and the product's public **changelog**, per project.
Everything is scoped by `workspace` + `project`. When the user doesn't name them, discover instead
of asking: `list_workspaces` → `list_projects` (both accept slugs or ids), then remember the pair
for the session.

## Triage requests

1. `list_requests` with `status: ["OPEN"]` (optionally `kind` / `horizon` / `size` / `impact` /
   `search`). The list is deliberately COMPACT (id, refCode, kind, status, severity, horizon,
   realitySize, realityImpact, title, commentCount, mergedIntoTicketId, area, createdAt, updatedAt,
   shippedAt) so a full board fits in context, don't expect bodies here. `updatedAt` is when the
   request last moved, `shippedAt` when it reached production (null until then), `area` its
   product area (its own, else its feature's). It returns a page
   `{ requests, offset, limit, hasMore }`, page with `offset` while `hasMore` is true. Without a
   `status` filter only the live lanes come back (CLOSED/DECLINED excluded). `size` (XS–XL) and
   `impact` (MINIMAL–VERY_HIGH) are any-of bands over the AI reality read:
   `size: ["XS","S"], impact: ["HIGH","VERY_HIGH"]` is the quick-wins query (requests not yet
   assessed never match either).
2. Summarize as a short table: title, kind, severity. Propose an action per item: don't act yet.
3. Act only on what the user confirms:
   - `set_request_status`: `PLANNED` (accept onto the roadmap), `CLOSED` (done/archived),
     `DECLINED` (**requires** `declinedReason`).
   - Never try to set `BUILDING`/`SHIPPED`, they're derived from real code signals.
4. `get_request` before judging a specific item, the detail carries the journey, comments, and the
   AI reality read (already-built? effort estimate).

## Groom the board (horizon triage)

`update_request` is the grooming tool, re-grade where a request sits or fix its definition, with
the same semantics as the in-app actions:

- `horizon` (`NOW` / `NEXT` / `VISION`, optionally with `size` XS–XL / `fit` CORE–OFF_CORE /
  `impact` MINIMAL–VERY_HIGH) pins a human override, the AI re-assessment won't flip it afterwards.
  `impact` is how much the request MOVES the product once shipped, independent of effort: a one-line
  fix can be `HIGH`, a month-long build `LOW`.
- `title` / `body` / `severity` edit the definition (re-embeds the intent and re-grounds the
  reality read, like an in-app edit).
- At least one field is required. The flow: compact `list_requests` → `get_request` on the items
  that matter → `update_request` to re-grade or reword.

## File a request

`create_request` with `kind` (`BUG` / `REQUEST`), a crisp `title` (≤200 chars), and a `body` with
repro steps (bug) or the ask + rationale (request). Exact-title dupes return the existing open
ticket: surface that instead of filing again.

## Report back onto a request

`add_request_comment` to leave findings ("verified in `<file>:<line>`, the guard already handles
this") so the team sees the evidence in the app. `@Name` mentions ping that member.

## Close the loop from a commit or PR

featury advances tickets from **code signals**. When you commit work that addresses a request, cite
its `refCode` (from `list_requests` / `get_request`, e.g. `idea/dark-mode`, `bug/login-white-screen`)
in the commit or PR message with a GitHub-style keyword:

```
Closes idea/dark-mode
Fixes bug/login-white-screen
Resolves change/new-onboarding
```

- Case-insensitive; a colon after the keyword (`Closes: idea/x`) is fine; one message can ref several.
- The slug alone resolves the ticket, so habit aliases (`feat/`, `fix/`, `issue/`) still match, but
  prefer the exact `refCode`.
- An explicit ref **auto-ships** the ticket (SHIPPED, "In production"; a bug reads "Fixed") and
  notifies the requester. Without one, featury falls back to inferred matching, which only
  _proposes_ a match for a human to confirm.
- Don't invent other conventions (no `Refs:` footers, ticket UUIDs, or REQ-123 codes), they link
  nothing. This section is the convention; never go searching the web for it.

## Answer "what exists / what shipped / how does X work"

- `get_product_overview`: what the product IS, in the team's own synthesized words. The cheapest
  orientation read on an unfamiliar project; take it before filing a request or judging whether a
  change fits.
- `list_features`: what the codebase has (the inventory). Returns a page
  `{ features, offset, limit, hasMore }` (default `limit` 50, max 500, page with `offset`).
  `list_areas` gives the vocabulary above it: the areas features are clustered into, whose `title`
  is exactly what a feature's `area` holds. The taxonomy is fluid: read it, don't assume.
- `get_feature`: one feature in full. `evidence` file paths are the fastest route from a product
  concept to the code that implements it, and `contributors` answers "who should review this?".
  Pass `changeLimit: 0` when you only want the definition.
- `recent_changes`: what shipped lately, in plain terms. Returns a page
  `{ items, total, limit, offset }` (default `limit` 50, max 200, page with `offset`); each item
  carries its feed-curation `visibility` mark (`PUBLIC`/`INTERNAL`) plus `delivery` and `features`
  context. Filter by `kind`, `impactSurface`, or an ISO 8601 `from`/`to` created-at range.
- `list_in_flight`: what's being built RIGHT NOW: open pull requests and release lanes, mapped to
  areas + features from the diff (no LLM, so it's cheap and current). Check `isLane` first: a lane
  row IS the release lane, so its `commitsAhead` and `mergedWork` are what's waiting to be promoted;
  reporting a lane as "someone's pull request" is the easy mistake here. On work rows,
  `hasUnmappedWork: true` means it touches code outside any known feature.
- `ask_featury`: open-ended codebase questions ("how does billing retry work?"). It runs a full
  agent turn and spends the workspace AI budget, so prefer the direct tools for factual lookups.
  Keep the returned `conversationId` to ask follow-ups in the same thread.

## Run the changelog

The changelog is the product's public page: AI folds a window of public changes into an **edition**,
and it goes out either when a person publishes it or when its **review window** expires. Reading is
open to any member; every write below needs **MANAGER or above**.

`get_changelog` is the one read, the public page's state and URLs, the rhythm, the notes, what's
pending, the draft **with its entries**, and the published history. Start here, always: every write
tool replaces rather than merges.

**Steer the writer with notes.** `set_changelog_notes` holds the product's standing instructions,
read by both AI passes (what counts as public at all, and how entries are worded). This is the one
thing an agent working in the repo knows that featury can't derive from a diff.

- Guidance, never facts: "never mention the admin console", "say organization, not workspace",
  "keep entries to one line". **Never** write what shipped, that comes from the repository, and a
  note claiming a release will not put one on the page.
- It replaces the whole note (max 2000 chars, `null` clears). Read the current value and send the
  merged text when adding a line.
- It lands on the NEXT draft. An open draft was already folded and is deliberately not re-folded, so
  say that rather than letting the user wait for a change that isn't coming.

**Set the rhythm, don't cron the publish.** `set_changelog_cadence` takes `cadence`, `weekday`
(UTC), `draftHour` (0–23, UTC (when the draft lands), `publishHour` (0–23, UTC) when a review
window closes), and `autoPublishDays`: the days a draft waits before publishing itself (`0` = the same day, so
a team that reviews in the morning can ship by evening). If the
user wants the changelog to go out automatically, that's the review window, not a scheduled publish
call: it gives a person a stated number of days to intervene. `autoPublishDays: null` means a person
publishes, and also **holds** an open draft that was already counting down, the way to stop an
edition that's about to go out.

**The edition lifecycle**, in order:

1. `prepare_changelog_edition` opens the next edition and starts the AI fold (spends budget; returns
   `generationStatus: "QUEUED"`, then `QUEUED` or `RUNNING`, `RETRYING` after a transient failure,
   while the fold runs and `SUCCEEDED` when it lands: poll `get_changelog`). It **discards any open
   draft**, including a reviewer's edits, so check `draft` first and confirm with the user before
   re-rolling one.
2. `update_changelog_edition` edits the draft: rename it, reword/reorder/drop entries. Full replace,
   so send the whole set. This is where you fix a fold that describes a revert as a feature, you
   were there when the code shipped, so check the entries against what actually happened.
3. `publish_changelog_edition` makes it public: it takes the next number, gets its permalink, goes
   out on RSS/JSON, and **turns the public page on** if it was still off. Read the draft before
   calling this, and don't publish on the user's behalf unless they asked for that specific edition
   to go out.
4. `unpublish_changelog_edition` is the undo, for the most recent edition only, and it refuses while
   a draft is open. A published edition can never be rewritten in place, permalinks and RSS mean
   people have already read it; unpublish, edit, republish.

## Manage outbound webhooks

featury can POST signed product events (`delivery.shipped`, `request.created`,
`request.status_changed`, `changelog.published`) to the user's own endpoints. All webhook tools
require the key owner to hold **MANAGER or above**, a permissions error means exactly that.

- `list_webhook_endpoints` → the project's endpoints. `disabledReason: "auto"` means the circuit
  breaker turned one off after sustained failures, revive it with
  `update_webhook_endpoint { enabled: true }` once the receiver is fixed.
- `create_webhook_endpoint` (public HTTPS `url`, optional `label` + `events` subset) returns
  `{ secret, record }`. The signing secret appears EXACTLY ONCE, relay it to the user immediately
  (it can only be rotated, never re-read). Same one-time rule for `rotate_webhook_secret`.
- `test_webhook_endpoint` sends a signed ping synchronously and returns `{ ok, status, error }`,
  the "is the receiver wired up?" check after create or a fix.
- Debug a receiver with `list_webhook_deliveries` (status, attempts, HTTP code, error) and
  `get_webhook_delivery` (the exact JSON payload that was sent).
- Signature scheme, envelope, and retry policy: https://featury.app/en/docs/api (§ Outbound webhooks).

## Signing in with no browser

Claude, ChatGPT and other clients that support MCP sign-in need nothing from you: given
`https://api.featury.app/mcp`, they open featury's own page and the user says yes there. When
you run where no browser can come back to you (a server, a container, an SSH session) and the
user has no API key to paste, sign in with a short code:

1. `POST https://api.featury.app/oauth/device_authorization` with the form body
   `client_id=featury-agent`. The answer carries `device_code`, `user_code` (like `WDJB-MJHT`),
   `verification_uri_complete`, `expires_in` (600 seconds) and `interval` (5 seconds).
2. Show the user the link and the code. Ask them to open the link on any device where they are
   signed in to featury, check that the page shows the same code, and press Connect. Never open
   the link for them or send it to anyone else.
3. Every `interval` seconds, `POST https://api.featury.app/oauth/token` with the form body
   `grant_type=urn:ietf:params:oauth:grant-type:device_code`, `device_code` and
   `client_id=featury-agent`. `authorization_pending` means keep waiting, and `slow_down` means
   you polled too soon. `access_denied`, `expired_token` or `invalid_grant` means stop and tell
   the user.
4. The answer's `access_token` is an ordinary `fk_` API key, named "AI agent (device sign-in)".
   It is handed out once, so save it where your MCP client reads it, and send it as
   `Authorization: Bearer fk_…` to `/mcp`. The user can revoke it under Account → API keys.

## Acting as the user

Every tool answers `{ data }` (the shapes above are what is inside it), or a tool error carrying
`{ error: { code, message } }`. Every call runs as the API key's owner under their permissions. A
`Workspace not found` / `Insufficient permissions` tool error means exactly that for the key's
owner: tell the user, don't retry blindly. `RATE_LIMIT_EXCEEDED` clears on its own: wait the
`details.retryAfterSecs` it carries, then retry. A transport-level failure (`fetch failed` and the like) is transient: retry
once, and if it still fails, say so and move on, don't burn calls on web searches for featury
itself; this skill and `https://featury.app/en/docs/mcp` are the authoritative docs.
