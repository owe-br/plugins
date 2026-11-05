---
name: smartgenius
description: "Make Instagram posts, carousels, stories, blog articles and standalone AI images with SmartGenius over its MCP tools (or its REST API). Use when the user asks to draft a post or carousel for one of their Instagram profiles, to draft a blog article for a profile that has a blog, to set up a profile for a brand with no Instagram, to make an image in a brand's style, or to generate any image at all from a prompt. Requires the smartgenius MCP server or a SmartGenius API key (setup guide: https://smartgenius.app/en/docs)."
---

# SmartGenius workflows

SmartGenius is a social media manager for Instagram. A key belongs to one **Espaço** (workspace)
and acts as the person who made it. The Espaço holds one or more **profiles**, each with its own
voice, colors and visual style. Most are Instagram accounts. A profile can also be a brand with no
Instagram, and some profiles have a **blog** (see "Blogs" below).

Two facts shape every call:

- **Posts and articles land as drafts.** You can make one; you can never approve, schedule or
  publish it. A person does that in the studio, at its `studioUrl`. Always hand that link back.
- **Everything costs credits from the monthly quota.** One credit is one image: one per slide of
  a post, one per `generate_image` image. An article costs more (see below). A failed image is not
  charged. `get_usage` shows what is left; check it before a large batch.

## Make a post

1. `list_profiles`: pick the profile. If there is more than one and the user did not name one,
   ask which. Every other tool takes its `profile` (with or without the `@`). Posts need a
   profile with `hasInstagram: true`: `create_post` refuses any other, before it charges anything.
2. `create_post` with `profile`, `idea` (a sentence or a paragraph: what the post is about) and
   a `requestId` you make up (a new UUID). Optional: `format` (`carousel` by default, `post` or
   `story`), `slides` (carousel only), `objective`, `tone`, `cta`, and `links` (up to 5 pages SmartGenius
   reads before planning). It answers at once with the post's `id`, before anything is drawn.
   No idea yet? Send `research: true` instead of `idea` (see "No idea yet" below).
3. `get_post` with `profile`, `postId` (that `id`) and `wait: 30`. Repeat while `making.status` is `queued` or
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

1. `list_profiles`: pick a profile whose `blog` is not null.
2. `create_article` with `profile`, `idea` (what the article is about, up to 2,000 characters)
   and a `requestId` you make up. It answers at once, with the article's `id` and `credits`
   (what the call cost), before anything is written. No idea yet? Send `research: true`
   instead of `idea` (see "No idea yet" below).
3. `get_article` with `profile`, `articleId` (that `id`) and `wait: 30`. Repeat while
   `making.status` is `queued` or `running`. An article takes a few minutes.
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
- `blogId`: the blog's `id` from `list_profiles`. The call is refused, before it charges, if the
  profile's blog was replaced since you read it.

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

| Code                            | What to do                                                                                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `UNAUTHORIZED`, `INVALID_TOKEN` | The sign-in or key is missing, revoked, or its maker left the Espaço. Ask the user to sign in again (or for a new key). Do not retry.       |
| `FORBIDDEN`                     | The key's maker lacks the right in this Espaço (an approver cannot spend credits, and only an admin can `create_profile`). Tell the user; do not retry. |
| `PAYMENT_REQUIRED`              | `create_profile`: the plan has no room for another profile. `details.upgrade` names the plan that does. Tell the user; waiting does not help.  |
| `NOT_FOUND`                     | Wrong profile, post or article id. Run `list_profiles` and check the `@`. `create_article` also answers it for a profile with no blog. If every blog call answers it, the Espaço has no blogs yet: tell the user. |
| `VALIDATION_ERROR`              | A field is wrong; `details` says which. Fix it and call again. Or the `requestId` was already used for a different request: make a new one. |
| `CONFLICT`                      | The first call with this `requestId` is still running: wait `retryAfterSecs`, then call again with the same `requestId`. After a `create_profile` that stopped halfway, `details` names the profile: call again with the same `requestId` to finish. |
| `QUOTA_EXCEEDED`                | No credits left this month or today (an article needs 2, or 3 with a cover). Tell the user when they are back (`details.resetAt`). Do not retry before then. |
| `RATE_LIMIT_EXCEEDED`           | Wait `retryAfterSecs` seconds, then retry once.                                                                                             |
| `GENERATION_FAILED`             | The image model failed or refused the prompt. Nothing was charged. Retry once; if it refuses again, change the prompt.                      |

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

| MCP tool         | REST                                                                                                |
| ---------------- | --------------------------------------------------------------------------------------------------- |
| `list_profiles`  | `GET /v1/profiles`                                                                                  |
| `create_post`    | `POST /v1/profiles/{profile}/posts`                                                                 |
| `get_post`       | `GET /v1/profiles/{profile}/posts/{id}?wait=30`                                                     |
| `create_article` | `POST /v1/profiles/{profile}/articles` (blogs only)                                                 |
| `get_article`    | `GET /v1/profiles/{profile}/articles/{id}?wait=30` (blogs only)                                     |
| `create_profile` | `POST /v1/profiles` (blogs only, admin only)                                                        |
| `generate_image` | `POST /v1/images`                                                                                   |
| `get_usage`      | `GET /v1/usage`                                                                                     |
| -                | `GET /v1/profiles/{profile}/posts/{id}/export?size=4:5` (a zip: one JPEG per slide + `caption.txt`) |

Success answers are `{ "data": … }`.

## Never

- Never tell the user a post or an article was published or scheduled. It is a draft until a
  person acts on it.
- Never call `create_post` or `create_article` again to "retry" a slow one. Wait on the one you
  have.
- Never call `create_post` for a profile with `hasInstagram: false`.
- Never make a new profile to "retry" a `create_profile` that stopped halfway. Use the same
  `requestId`.
- Never promise rankings, traffic or visitors from an article.
- Never retry a spending call with a new `requestId`: the same one is what makes it safe.
- Never loop `generate_image` to get a variation the user did not ask for: each image is quota.
- Never print, log or commit the `sg_` key.
