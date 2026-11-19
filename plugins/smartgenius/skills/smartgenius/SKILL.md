---
name: smartgenius
description: "Use SmartGenius to draft Instagram posts, carousels, stories or blog articles, generate images with or without a brand profile, or set up a brand without Instagram. Read a profile's connection status, posting habits, post performance, suggestions and Autopilot schedule. When someone asks to connect or reconnect Instagram, get a private link for them to open. Requires the smartgenius MCP server or a SmartGenius REST API key (setup: https://smartgenius.app/en/docs)."
---

# SmartGenius workflows

SmartGenius is a social media manager for Instagram. A key belongs to one **Espaço** (workspace)
and acts as the person who made it. The Espaço holds one or more **profiles**, each with its own
voice, colors and visual style. Most are Instagram accounts. A profile can also be a brand with no
Instagram, and some profiles have a **blog** (see "Blogs" below). A profile is a brand, and a
brand can publish to more than one Instagram account or blog (see "A brand with more than one
account or blog" below).

Two facts shape every call:

- **Posts and articles land as drafts.** You can make one; you can never approve, schedule or
  publish it. A person does that in the studio, at its `studioUrl`. Always hand that link back.
- **Making content costs credits from the monthly quota.** One credit is one image: one per slide
  of a post, one per `generate_image` image. An article costs more (see below). A failed image is
  not charged. `get_usage` shows what is left; check it before a large batch. Reading costs
  nothing (see "Read what SmartGenius knows").

## Read what SmartGenius knows

Five tools only read. They spend no credits, change nothing and never reach Instagram, so call
them whenever they help: before you plan a post, or when the user asks how a profile is doing or
what is coming up. Each takes `profile`.

- `get_profile`: the profile's `language` and `timezone`; `instagram` (`connected`, `username`,
  `needsReconnect`, `canPublish`, `publishingEnabled`, `canReadInsights`, `connectedAt`); and
  `learned`, what SmartGenius learned from its posts: `subjects` (each with a `weight` from 0 to
  1), `captionTone`, `cadence`, `topHashtags` and `scannedAt`. `cadence` has `postsPerWeek` and
  the `postingDays` and `postingHours` it posts most (hours in `timezone`): when it posts, not when
  posting works best. When `needsReconnect` is true, tell the user the account needs to be
  reconnected. If they ask to reconnect it, use the steps under "Connect Instagram".
- `list_posts`: the profile's posts, newest first, with `status` (`draft`, `ready` meaning
  approved, `scheduled`, `publishing`, `published` or `failed`), `scheduledAt`, `publishedAt`,
  `permalink` and `studioUrl`. Pass `status: ["scheduled"]` for what is booked to go out, `q` to
  search, and `limit` (up to 50) with `offset` to page. `total` counts every match. Read one in
  full with `get_post`.
- `list_media`: the profile's own Instagram posts, newest first: `kind`, `postedAt`, `permalink`,
  the first 300 characters of the `caption`, the `subjects` SmartGenius saw in the pictures, and
  `numbers` (`reach`, `saved`, `shares`, `likes`, `comments`, `totalInteractions`, and `views` for
  reels) as of `numbersAt`. `madeHere` marks a post made in SmartGenius. Page with `cursor` (the
  `nextCursor` you got) and `limit` (up to 48, default 24). `connected: false` means the profile
  has no working Instagram connection, and the list is empty.
- `list_suggestions`: what the profile's own posts and numbers suggest next, strongest first. Each
  one has a `kind` and its `facts`, never a sentence, so write the sentence yourself: `subject`
  (`subject`, and `weeks` since it was last posted), `cadence` (`was` and `now`, posts a week in
  the month before and in the last month), `format` (`posts` made without a single carousel),
  `repeat_winner` (a post about `subject` got `times` the profile's usual `metric`) and `template`
  (its post patterns were drafted from less than SmartGenius can read now). `postId` is set once a
  suggestion became a post.
- `get_routine`: the profile's Autopilot: `on`, its posting times (`rules`), `approval`
  (`required` waits for a person's ok, `tacit` goes out unless someone steps in, `none` goes out
  on its own), the saved `ideas` it uses first, the standing `instruction`, the next slots with
  what it would post in each (`preview`), the posts waiting for an ok (`waitingIds`), and `gate`,
  which says why it cannot run as set (null when it can). You cannot change Autopilot: send the
  user to the studio for that.

**Numbers need Instagram's permission.** `numbers` is null for a post whose numbers SmartGenius
never read. It reads them for recent posts, and only while `get_profile` says
`canReadInsights: true`. When they are missing, say so and never estimate them. `numbers: {}`
means Instagram answered with none.

Example: to suggest the next post, call `get_profile`, `list_posts` with `status: ["scheduled"]`,
`list_suggestions` and `get_routine`. Then propose an idea that fits the profile's `subjects` and
does not repeat what is already booked.

`list_brands` also only reads, and takes no `profile`: every brand of the Espaço with its
`profile` and the places it publishes to (`destinations`). Each Instagram account has `kind`,
`id`, `name`, `connected` and `needsReconnect`; each blog has `kind`, `id`, `name`, `url` and
`state`.

## A brand with more than one account or blog

Most brands have one Instagram account and at most one blog, and every call works with just
`profile`. When `list_brands` shows a brand with two or more accounts, or two or more blogs, name
the one the user means:

- `create_post` takes `instagram`: the account's `id` from `list_brands`.
- `create_article` takes `blogId`: the blog's `id` from `list_brands`.

If the user did not say which, ask them. Never pick one yourself. A call that names none when
there are several answers `VALIDATION_ERROR`, and `details.choices` lists each place (`kind`,
`id`, `name`): nothing was made and nothing was charged. Ask the user which one, then call again
with its `id` and the same `requestId`.

The draft lives on that place. The `create_post` or `create_article` answer says where it went
(`destination`) and gives a `profile` to read it back with: the handle for the brand's own place,
or an id for one of its other places. Use that `profile` for `get_post` and `get_article`, and
hand the user the answer's `studioUrl`.

## Connect Instagram

`get_instagram_connect_link({"profile":"forno.da.vila"})` returns `profile`, `url` and `expiresAt`.
It costs no credits and returns no Instagram access token. Only the Espaço's owner or an admin
can request it. Their account, admin access and the key that made the link must still be active
when the connection finishes.

1. Use `list_profiles` to choose the profile the user wants to connect. Request the link only
   when they ask to connect or reconnect Instagram, never as part of an inventory read. To
   connect one of a brand's other accounts, pass that account's `id` from `list_brands` as
   `profile`.
2. For a reconnect, tell them to choose the same Instagram account. Approving a different account
   replaces the connection and removes the previous account's imported data from SmartGenius.
   Give them the private `url` and ask them to open it and complete Meta's approval themselves.
   Do not open or approve it for them. Creating the link does not connect anything.
3. The link expires at `expiresAt` (ISO 8601 UTC, currently ten minutes after creation). If it
   expires, request a new link. A new call gets a current link; do not reuse an expired one.
   If access was removed, ask a current workspace admin to start the connection instead.
4. After they finish, call `get_profile` again to check the connection and insights access. A link
   being opened or its window closing is not proof that the account is connected.

The link reaches the connected app's company. Share it only with the person completing approval;
never put it in logs, public posts or saved task notes. Meta returns the person to this profile's
connection screen in the studio. Do not claim success from the link alone.

For REST, use `POST /v1/profiles/{profile}/instagram/connect` with no body or `{}`.
Send no `returnTo` or `requestId`; SmartGenius chooses the return screen.

## Make a post

1. `list_profiles`: pick the profile. If there is more than one and the user did not name one,
   ask which. Every other tool takes its `profile` (with or without the `@`). Posts need a
   profile with `hasInstagram: true`: `create_post` refuses any other, before it charges anything.
   If `list_brands` shows the brand with more than one Instagram account, ask which one and pass
   its `id` as `instagram`.
2. `create_post` with `profile`, `idea` (a sentence or a paragraph: what the post is about) and
   a `requestId` you make up (a new UUID). Optional: `format` (`carousel` by default, `post` or
   `story`), `slides` (carousel only), `objective`, `tone`, `cta`, `instagram`, and `links` (up to 5 pages SmartGenius
   reads before planning). It answers at once with the post's `id`, before anything is drawn.
   No idea yet? Send `research: true` instead of `idea` (see "No idea yet" below).
3. `get_post` with `profile` (the one the `create_post` answer gave), `postId` (that `id`) and `wait: 30`. Repeat while `making.status` is `queued` or
   `running`. A carousel takes a few minutes; tell the user it is on its way instead of going
   quiet.
4. When it is `done`, show the user the slides' text, the caption and the `studioUrl`. If it
   `failed`, say so with `making.failure` and offer to try again. `cancelled` means a person
   stopped it in the studio: leave it.

**No idea yet.** `create_post` and `create_article` take `research: true` in place of `idea`:
SmartGenius picks the subject itself, the one its own schedule would pick now (the profile's
saved ideas first, then today's research on its niche, a date, its numbers, its own subjects).
Send one of the two. With neither, the call is a `VALIDATION_ERROR`; with `research: true` and
nothing to pick from, a `CONFLICT`. Neither is charged. A typed `idea` always wins: ask the user
for one when they have something in mind.

**One post, one `requestId`.** If a `create_post` call times out or its answer is lost, call it
again with the SAME `requestId`: you get the first answer back and nothing is spent twice. A
new `requestId` (or none) makes a second post and spends the images again. The id is kept for
24 hours.

## Blogs

`list_profiles` shows each profile's `hasInstagram` and its `blog`: `id`,
`name`, `url` and `state` (`soon` before the first article is published, then `live`, or `off`),
or `blog: null` when the profile has none. A profile with `hasInstagram: false` is a brand with
no Instagram: its `profile` is only its name in SmartGenius, never an `@`.

## Make a blog article

1. `list_profiles`: pick a profile whose `blog` is not null. If `list_brands` shows the brand
   with more than one blog, ask which one and pass its `id` as `blogId`.
2. `create_article` with `profile`, `idea` (what the article is about, up to 2,000 characters)
   and a `requestId` you make up. It answers at once, with the article's `id` and `credits`
   (what the call cost), before anything is written. No idea yet? Send `research: true`
   instead of `idea` (see "No idea yet" below).
3. `get_article` with `profile` (the one the `create_article` answer gave), `articleId` (that
   `id`) and `wait: 30`. Repeat while `making.status` is `queued` or `running`. An article takes
   a few minutes.
4. When `making.status` is `succeeded`, show the user the `title`, the `dek`, the `body` and the
   `studioUrl`. If it is `failed`, say so with `making.failure` and offer to try again; credits
   that went unused are refunded. `cancelled` means the run was stopped: leave it.

Example: `create_article` with `profile: "your.brand"`, `idea: "Why homemade bread goes stale"`
and `requestId: "3f6c…"`. The answer has `state: "draft"`, `making.status: "queued"`,
`credits: 2` and the `studioUrl`.

**The cost.** The text costs 2 credits. A newly drawn cover costs 1 more, and only when you send
`drawCover: true` (the default is `false`: no cover is drawn). A refused call is not charged. Tell
the user the cost before a large batch.

Optional fields of `create_article`:

- `links`: up to 3 pages SmartGenius reads before it writes.
- `language`: `pt-BR`, `en` or `es`. The default is the profile's language.
- `adFor`: set it when the article is an ad for a brand. The name is shown to readers.
- `fromPostId`: the id of a post on this profile to build the article from. Its links come along
  and count against the 3.
- `ideaId`: the id of an idea saved on this profile's blog. The idea is used up.
- `blogId`: the blog's `id` from `list_profiles` or `list_brands`. Required when the brand has
  more than one blog. The call is refused, before it charges, if the brand no longer has that
  blog.

**One article, one `requestId`.** Same rule as a post: after a timeout or a lost answer, call
`create_article` again with the SAME `requestId` and you get the first article back, with nothing
spent twice. A new `requestId` (or none) makes a second article and spends again. Keep the body
the same too: the same `requestId` with another body is a `VALIDATION_ERROR`.

**What `get_article` returns.** `state` (`draft`, `approved`, `scheduled`, `publishing`, `live`,
`live_changed`, `off` or `failed`), `making`, `title`, `dek`, `body`, `links`, `tags`, `language`
and `studioUrl`. The `body` is a small Markdown subset: paragraphs, `##` headings, lists (`- ` or `1. ` lines),
quotes (`> ` lines) and links. A link in it looks like `[words](L3)`: `L3`
is the `id` of an entry in `links`, which has the `label` and the real `href`. `get_article` only
reads. It never makes a second article.

**You never publish it.** No tool approves, schedules or publishes an article, and an article made
here has no slot or deadline. Hand the user the `studioUrl`. There they read it, change it and
approve it. It goes live only when a person approves it, or when the blog's own schedule, which a
person already set up, takes it.

Do not promise that an article will rank on Google or bring visitors. SmartGenius promises
neither.

## Make a profile with a blog

`create_profile` makes a profile for a brand with no Instagram and, when you pass `blog`, its
blog. **Only an admin of the Espaço can call it.** It counts against the plan's profile limit. It
reads no website, buys no article and asks for no Instagram login.

Example: `create_profile` with `requestId: "9a1d…"`, `name: "Padaria da Vila"` and
`about: "A bakery in São Paulo that sells sourdough bread."`. The answer has `profile` (the name
to use in the other tools), `hasInstagram: false`, `created: true` and the `studioUrl`.

- `requestId` is **required**. It is what stops a lost answer from making a second profile.
- `name` (up to 80 characters) and `about` (up to 500) describe the brand.
- Optional: `primaryColor` (like `#1b6ef3`), `language` and `handle` (a-z, 0-9, dots and
  underscores; the default is made from `name`; it is not an Instagram `@`).
- Optional `blog`: `name` and `label` are required. `label` is the first part of the blog's
  address: 3 to 63 letters, digits and hyphens. A label that is taken or reserved fails the blog
  step (see below). Also optional: `about`, `parentUrl` (the brand's own website, https) and
  `contact`.
- Optional `blog.customHost`: the user's own domain for the blog, like `blog.example.com`. It
  needs `blog`, and it only starts the connection. The answer's `customDomain.cname` is the value
  to put in that domain's DNS, and `customDomain.status` says where it stands. The domain is live
  only when the status is `active`. Ask the user to add the record, or to finish in the blog's
  settings in the studio. You cannot check their DNS for them.

**If it stops halfway.** The profile is made first, then the blog, then the domain. If the blog or
the domain step fails, the answer is `CONFLICT` (409) and its `details` name the profile that
exists: `profile`, `studioUrl`, `done` and `stoppedAt`. The profile is real, so do not start over.
Fix what the message says and call `create_profile` again with the SAME `requestId`, the same
`name` and the same `handle`. It finds the profile, skips the steps that are done and finishes the
rest. A new `requestId` would make a second profile.

## Make an image

`generate_image` with a `prompt` and a new `requestId`. Optional: `count` (1–4, default 1),
`aspectRatio` (`1:1` default; `4:5`, `3:4`, `9:16`, `16:9`, `4:3`, `3:2`, `2:3`), and `profile`.
A retry after a timeout uses the same `requestId`, and gets the same images back.

- **Without `profile`** the prompt reaches the image model exactly as written. Use this for any
  image at all, even one with nothing to do with Instagram or the user's business.
- **With `profile`** the image is drawn in that profile's look (its visual style and colors).
  Use it when the image is for that brand.

The answer carries one `url` per image. **The links expire in 7 days**, and the files are deleted
after that: download them now if the user needs them later.

## Errors

A REST error is `{ "error": { "code", "message", "details" } }`. Over MCP the same object comes
back with `isError: true`. Act on the code:

| Code                            | What to do                                                                                                                                                                                                                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `UNAUTHORIZED`, `INVALID_TOKEN` | The sign-in or key is missing, revoked, or its maker left the Espaço. Ask the user to sign in again (or for a new key). Do not retry.                                                                                                                                     |
| `FORBIDDEN`                     | The key's maker lacks the right in this Espaço (an approver cannot spend credits, and only an admin can `create_profile` or `get_instagram_connect_link`). Tell the user; do not retry.                                                                                   |
| `PAYMENT_REQUIRED`              | `create_profile`: the plan has no room for another profile. `details.upgrade` names the plan that does. Tell the user; waiting does not help.                                                                                                                             |
| `NOT_FOUND`                     | Wrong profile, post or article id. Run `list_profiles` and check the `@`. `create_article` also answers it for a profile with no blog. If every blog call answers it, the Espaço has no blogs yet: tell the user.                                                         |
| `VALIDATION_ERROR`              | A field is wrong; `details` says which. Fix it and call again. Or the `requestId` was already used for a different request: make a new one. When `details.choices` lists accounts or blogs, ask the user which one and call again with its `id`; never pick one yourself. |
| `CONFLICT`                      | The first call with this `requestId` is still running: wait `retryAfterSecs`, then call again with the same `requestId`. After a `create_profile` that stopped halfway, `details` names the profile: call again with the same `requestId` to finish.                      |
| `QUOTA_EXCEEDED`                | No credits left this month or today (an article needs 2, or 3 with a cover). Tell the user when they are back (`details.resetAt`). Do not retry before then.                                                                                                              |
| `RATE_LIMIT_EXCEEDED`           | Wait `retryAfterSecs` seconds, then retry once.                                                                                                                                                                                                                           |
| `GENERATION_FAILED`             | The image model failed or refused the prompt. Nothing was charged. Retry once; if it refuses again, change the prompt.                                                                                                                                                    |

## Limits

- 120 calls a minute per key.
- 5 `get_post` or `get_article` waits at once per key, counted together. A sixth answers right
  away without waiting, so wait on one post or article at a time.
- `wait` is at most 50 seconds per call.

## Signing in

Claude, ChatGPT and other clients that support MCP sign-in need nothing from you: given
`https://api.smartgenius.app/mcp`, they open SmartGenius's own page and the user presses Allow
there. In Codex, the user runs `codex mcp login smartgenius` (Codex 0.147 or later). Either way
SmartGenius makes a key named after the app, which a workspace admin can revoke under API and MCP
in the workspace menu.

Only an admin of the Espaço can connect an app. Anyone else sees a page that says so: tell them to
ask an admin of their Espaço to connect it, or to make them an admin.

## Signing in with no browser

When you run where no browser can come back to you (a server, a container, an SSH session) and
the user has no API key to paste, sign in with a short code:

1. `POST https://api.smartgenius.app/oauth/device_authorization` with the form body
   `client_id=smartgenius-agent`. Any other client id gets `unauthorized_client`. The answer
   carries `device_code`, `user_code` (like `WDJB-MJHT`), `verification_uri_complete`,
   `expires_in` (600 seconds) and `interval` (5 seconds).
2. Show the user the link and the code. Ask them to open the link on any device, sign in, check
   that the page shows the same code, pick the Espaço and press Allow. They can also go to
   https://my.smartgenius.app/device and type the code. Only an admin of the Espaço can allow it.
   Never open the link for them or send it to anyone else.
3. Every `interval` seconds, `POST https://api.smartgenius.app/oauth/token` with the form body
   `grant_type=urn:ietf:params:oauth:grant-type:device_code`, `device_code` and
   `client_id=smartgenius-agent`. `authorization_pending` means keep waiting, and `slow_down`
   means you polled too soon. `access_denied` or `expired_token` means stop and tell the user;
   a new attempt starts from step 1.
4. The answer's `access_token` is an ordinary `sg_` key named "AI agent (device sign-in)". It
   has no expiry and counts toward the Espaço's limit of 10 keys. It is handed out once, so save
   it where your MCP client reads it, and send it as `Authorization: Bearer sg_…` to `/mcp`. A
   workspace admin can revoke it under API and MCP in the workspace menu.

A workspace admin can also make a key by hand under API and MCP and give it to you.

## Without MCP

The same operations are REST routes on `https://api.smartgenius.app`, with the key as
`Authorization: Bearer sg_…`:

| MCP tool                     | REST                                                                                                |
| ---------------------------- | --------------------------------------------------------------------------------------------------- |
| `list_profiles`              | `GET /v1/profiles`                                                                                  |
| `list_brands`                | `GET /v1/brands`                                                                                    |
| `get_profile`                | `GET /v1/profiles/{profile}`                                                                        |
| `get_instagram_connect_link` | `POST /v1/profiles/{profile}/instagram/connect` (admin only)                                        |
| `list_posts`                 | `GET /v1/profiles/{profile}/posts?status=scheduled` (several states as a comma list)                |
| `list_media`                 | `GET /v1/profiles/{profile}/media?limit=24`                                                         |
| `list_suggestions`           | `GET /v1/profiles/{profile}/suggestions`                                                            |
| `get_routine`                | `GET /v1/profiles/{profile}/routine`                                                                |
| `create_post`                | `POST /v1/profiles/{profile}/posts`                                                                 |
| `get_post`                   | `GET /v1/profiles/{profile}/posts/{id}?wait=30`                                                     |
| `create_article`             | `POST /v1/profiles/{profile}/articles` (blogs only)                                                 |
| `get_article`                | `GET /v1/profiles/{profile}/articles/{id}?wait=30` (blogs only)                                     |
| `create_profile`             | `POST /v1/profiles` (blogs only, admin only)                                                        |
| `generate_image`             | `POST /v1/images`                                                                                   |
| `get_usage`                  | `GET /v1/usage`                                                                                     |
| -                            | `GET /v1/profiles/{profile}/posts/{id}/export?size=4:5` (a zip: one JPEG per slide + `caption.txt`) |

Success answers are `{ "data": … }`.

## Never

- Never tell the user a post or an article was published or scheduled. It is a draft until a
  person acts on it.
- Never call `create_post` or `create_article` again to "retry" a slow one. Wait on the one you
  have.
- Never call `create_post` for a profile with `hasInstagram: false`.
- Never pick one of a brand's accounts or blogs for the user. When there are several, ask.
- Never invent or estimate a number SmartGenius did not return. When `numbers` is null, say it has
  not read them.
- Never make a new profile to "retry" a `create_profile` that stopped halfway. Use the same
  `requestId`.
- Never promise rankings, traffic or visitors from an article.
- Never retry a spending call with a new `requestId`: the same one is what makes it safe.
- Never loop `generate_image` to get a variation the user did not ask for: each image is quota.
- Never print, log or commit the `sg_` key.
