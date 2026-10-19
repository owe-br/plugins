---
name: smartgenius
description: "Make Instagram posts, carousels, stories and standalone AI images with SmartGenius over its MCP tools (or its REST API). Use when the user asks to draft a post or carousel for one of their Instagram profiles, to make an image in a brand's style, or to generate any image at all from a prompt. Requires the smartgenius MCP server or a SmartGenius API key (setup guide: https://smartgenius.app/en/docs)."
---

# SmartGenius workflows

SmartGenius is a social media manager for Instagram. A key belongs to one **Espaço** (workspace)
and acts as the person who made it. The Espaço holds one or more **profiles** (Instagram
accounts), each with its own voice, colors and visual style.

Two facts shape every call:

- **Posts land as drafts.** You can make a post; you can never approve, schedule or publish it.
  A person does that in the studio, at the post's `studioUrl`. Always hand that link back.
- **Images cost quota.** Every image comes out of the Espaço's monthly quota: one per slide of a
  post, one per `generate_image` image. A failed image is not charged. `get_usage` shows what is
  left; check it before a large batch.

## Make a post

1. `list_profiles`: pick the profile. If there is more than one and the user did not name one,
   ask which. Every other tool takes its `profile` (with or without the `@`).
2. `create_post` with `profile`, `idea` (a sentence or a paragraph: what the post is about) and
   a `requestId` you make up (a new UUID). Optional: `format` (`carousel` by default, `post` or
   `story`), `slides` (carousel only), `objective`, `tone`, `cta`, and `links` (up to 5 pages SmartGenius
   reads before planning). It answers at once with the post's `id`, before anything is drawn.
3. `get_post` with `profile`, `postId` (that `id`) and `wait: 30`. Repeat while `making.status` is `queued` or
   `running`. A carousel takes a few minutes; tell the user it is on its way instead of going
   quiet.
4. When it is `done`, show the user the slides' text, the caption and the `studioUrl`. If it
   `failed`, say so with `making.failure` and offer to try again. `cancelled` means a person
   stopped it in the studio: leave it.

**One post, one `requestId`.** If a `create_post` call times out or its answer is lost, call it
again with the SAME `requestId`: you get the first answer back and nothing is spent twice. A
new `requestId` (or none) makes a second post and spends the images again. The id is kept for
24 hours.

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
| `FORBIDDEN`                     | The key's maker lacks the right in this Espaço (an approver cannot spend images). Tell the user; do not retry.                              |
| `NOT_FOUND`                     | Wrong profile or post id. Run `list_profiles` and check the `@`.                                                                            |
| `VALIDATION_ERROR`              | A field is wrong; `details` says which. Fix it and call again. Or the `requestId` was already used for a different request: make a new one. |
| `CONFLICT`                      | The first call with this `requestId` is still running. Wait `retryAfterSecs`, then call again with the same `requestId`.                    |
| `QUOTA_EXCEEDED`                | No images left this month or today. Tell the user when images are available again (`details.resetAt`). Do not retry before then.            |
| `RATE_LIMIT_EXCEEDED`           | Wait `retryAfterSecs` seconds, then retry once.                                                                                             |
| `GENERATION_FAILED`             | The image model failed or refused the prompt. Nothing was charged. Retry once; if it refuses again, change the prompt.                      |

## Limits

- 120 calls a minute per key.
- 5 `get_post` waits at once per key. A sixth answers right away without waiting, so wait on
  one post at a time.
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
| `generate_image` | `POST /v1/images`                                                                                   |
| `get_usage`      | `GET /v1/usage`                                                                                     |
| -                | `GET /v1/profiles/{profile}/posts/{id}/export?size=4:5` (a zip: one JPEG per slide + `caption.txt`) |

Success answers are `{ "data": … }`.

## Never

- Never tell the user a post was published or scheduled. It is a draft until a person acts on it.
- Never call `create_post` again to "retry" a slow post. Wait on the one you have.
- Never retry a spending call with a new `requestId`: the same one is what makes it safe.
- Never loop `generate_image` to get a variation the user did not ask for: each image is quota.
- Never print, log or commit the `sg_` key.
