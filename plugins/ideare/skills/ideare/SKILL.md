---
name: ideare
description: "Work with a small business's brand on ideare over its MCP tools (or its REST API): read an approved brand and the link to each file (logo, site icons, share cards, social sizes, tokens, business card), put it in a codebase with `npx ideare init`, change the brand's draft, check it, ask the owner to approve, draw AI symbols and art in the brand's style, and make social posts from the brand's templates. Use when the user mentions their brand, logo, brand kit, colors, fonts, favicon or share card on ideare, an ideare.app/b/<slug> link, or asks to dress a site in their brand. Requires the ideare MCP server or an ideare API key (https://ideare.app/en)."
---

# ideare workflows

ideare makes a small business's brand kit: the logo in every version, colors and fonts, site
icons, share cards, every social size, an email signature, a business card and guidelines in
plain words. Every file is drawn from one `brand.json`, the **masters** (the format:
https://ideare.app/schema/brand.v1.json).

A key belongs to one **workspace** and acts as the person who made it, with their role there.
Three facts shape every call:

- **A brand has a private draft and public versions.** Saving the draft publishes nothing.
  Approved versions are public at `https://cdn.ideare.app/b/<slug>/v<n>/<path>`, never change,
  and `latest/` follows the current one.
- **You usually can't publish.** `approve_draft` from an agent becomes a proposal the owner
  approves in one tap in the studio (studio.ideare.app). Say so; never call it again to push it
  through.
- **Only AI pictures cost credits.** Reading, saving, checking and approving are free.
  `generate_symbols` costs 2 credits per idea (8 for a batch of 4); `generate_art` costs 1 at
  `1k` and 2 at `2k`. A picture that fails, or a symbol that shows letters, refunds all its
  credits. `get_usage` says what is left. A new account's welcome grant is 50 credits, valid for
  90 days, once per email address. That covers up to 25 symbols, not 50.

## Read a brand

1. `list_brands`: the brands in the workspace, with each one's `slug`, `currentVersion` (null
   until the first approval) and whether a proposal is waiting. If there are several and the user
   didn't name one, ask which.
2. `get_brand` with `slug`: the draft's `masters` and `rev`, the `currentVersion` and `urls`.
   `urls.page` is the brand's public page (ideare.app/b/<slug>): the one link to give anyone who
   helps (a developer, an AI site builder, a social media manager, a print shop).
3. `list_files` with `slug` (and `group` for one folder): every file of a version with its
   `url`, `mime`, `size` and `sha256`. The current version when you leave `version` out.

Where things are, under `v<n>/` or `latest/`:

| Group      | What                                                                                                  |
| ---------- | ----------------------------------------------------------------------------------------------------- |
| `logo`     | `logo.svg` for light grounds, `logo-dark.svg` for dark ones, `mark.svg`, `small.svg` (16-32 px), PNGs |
| `web`      | `favicon.ico`, `icon.svg`, `apple-touch-icon.png`, `site.webmanifest` and its icons                   |
| `og`       | `og.png` (the share card) and `og.<locale>.png`, each with an `.alt.txt`                              |
| `social`   | avatars, covers and banners per network, Instagram highlight covers, post and story backgrounds       |
| `tokens`   | `tokens.css`, `tailwind.css`, `brand.tokens.json` (DTCG), `fonts.css` and the font files              |
| `registry` | `theme.json`, a shadcn `registry:theme` item                                                          |
| `docs`     | `brand.md` (the guidelines), `brand.json` (the public masters), `head.html`, `prompt.md`              |
| `email`    | `signature.html` and its logo                                                                         |
| `print`    | the business card, front and back, at 300 dpi, in Brazilian, US and European sizes                    |

`get_version` and `list_versions` read approved versions of any brand, not only this
workspace's: versions are public.

## Put the brand in a codebase

Don't copy files by hand. In the project, run:

```sh
npx ideare init <slug>
```

It needs no account. It detects Next.js (App or Pages Router), Vite or plain HTML, prints the brand's name
and domain, lists every file it adds or replaces and backs up the project's own, then writes the
icons, the share cards, the theme tokens and `ideare.lock.json`. After that:

- `npx ideare pull` brings a newer approved version; `--frozen` installs exactly the lock.
- `npx ideare pull --pr` previews the approved files, then opens a draft GitHub pull request.
  It needs the user's git and GitHub CLI login, a committed cloud setup and the default branch's
  current tip. It works in a separate worktree, leaving the user's branch and staging area alone.
  Agents can pass `--yes --json`. Brand approval and code review are separate: a PR never approves
  a private brand draft.
- `npx ideare check` fails when a brand file was edited by hand. Put it in CI.
- With shadcn/ui: `npx shadcn@latest add https://cdn.ideare.app/b/<slug>/latest/registry/theme.json`.
- An AI site builder (Lovable, v0, Bolt) takes `docs/prompt.md` as it is.

## Change a brand

1. `get_brand`: keep the draft's `rev`.
2. `update_draft` with `slug`, `draftRev` (that `rev`) and the **whole** `masters`, changed. If
   someone saved in between you get `CONFLICT` with the current draft in `details`: apply your
   change to it and send again with its rev. Never resend your stale copy.
3. `check_brand`: the checks an approval runs (contrast, the logo at 16 px, text that fits, safe
   areas, the copy rules). Fix every result whose `status` is `fail`; each `message` says what to
   change. `warn` is advice.
4. `approve_draft` with `slug` and the `draftRev` you checked, plus an `idempotencyKey`:
   - `proposed`: the owner was asked. Tell the user the owner approves it in the studio, then
     stop.
   - `approving`: you may publish (an owner's or admin's own CLI sign-in). The files are being
     drawn; follow `runId` with `get_run` until it `succeeded`. One approval redraws every file.

Copy in the masters follows the brand's own rules: no em dash, no exclamation marks, sentence
case, and none of the words in `voice.neverSay`. `check_brand` flags a line that breaks them.

## Import an existing brand

Keep what the owner already uses. Do not send an existing brand through new-logo directions.

1. `import_brand` accepts up to 5 different public site or profile links in `links`, uploaded
   `files` (`assetId` and `path`) and optional local style files in `repo`. Use one request and one
   `idempotencyKey` for the combined import. Files can be uploaded through the studio, the CLI
   or the API's signed upload flow; a local filename alone does not send its bytes.
2. Follow its run, then `get_folder_import` with `runId`. It shows where each result came from,
   conflicting colors, fonts and words, and the original beside a traced logo. Keep uploaded
   originals first. A failed-quality trace is not permission to replace the owner's logo.
3. Let the owner choose where findings differ, then `apply_import` with a fresh `idempotencyKey`,
   `runId` and the review's `moves`, `licensed` and `choices`. Use the choice IDs the review returns.
   For an existing draft,
   include its `draftRev`. This saves one private draft, never a public version.
4. A failed link does not discard the rest. Continue with `import_brand`, `retryOf` set to the
   review's run ID, and only failed links or genuinely new assets. If that continuation's answer
   is lost, retry its same payload and key, not a fresh import.

A repository is another input, not a URL we clone or execute. Locally,
`npx ideare init --from-code` reads CSS colors, Tailwind settings and logo files.
Over MCP, `read_repo` reads selected style-file excerpts and returns colors and font choices;
`import_brand` can include the same files in `repo` for one combined review. Never send env files,
credentials or the whole repository. To keep a logo, upload its actual file too.

Imports and draft writes need a key allowed to write. Free-plan keys only read; an owner can
use the studio's import flow for free.

## Start a new brand

The studio (studio.ideare.app) is the easy path: it draws 3 or 4 complete looks from a name and
an idea, and the owner picks one. From here:

- `generate_text` with `idea` (and `name`, `locales`): names, taglines, a voice, palette
  directions and a font pair. Free, under a daily allowance.
- `check_names` with up to 5 `names`: domains and social handles. `available` means no record
  was found: say "looks free", never promise it. It links trademark searches; it is not legal
  advice.
- `import_link` with a site or a profile (`padaria.com.br`, `@padaria`): its name, colors and
  logo, as a run.
- `create_brand` with `name` (and `slug`, `masters`): a private draft. Without `masters` it starts
  from the name alone and `check_brand` lists what is missing. Send the user to the studio to
  pick a look, or write complete masters yourself following the schema.

## AI symbols and art

1. Check `get_usage` before a batch. Say the full cost before you call: 2 credits per symbol,
   so 4 symbols cost 8 credits. The 50-credit welcome grant covers up to 25 symbols.
2. `generate_symbols` with `slug`, `count` (1 to 4) and an optional `hint` ("a coffee bean"), or
   `generate_art` with `slug`, `prompt` and `size`. Always send an `idempotencyKey` you make up
   (a new UUID per request). The answer is a run, with what it charged in `meta.credits`.
3. `get_run` with the run's `id` every few seconds until `status` is `succeeded`, `failed` or
   `cancelled`. Symbols take seconds each. Tell the user it is on the way instead of going quiet.
   Where your client shows pictures, the finished run comes with previews.
4. A symbols run's `result.symbols[]` has each idea's `concept` and a clean `svg`. To use one,
   put it in the masters as `mark.svg` with `mark.source.kind` set to `ai`, then `update_draft`.
   An art run's `result.assetId` is in `list_assets`, with a download link that expires.

To stop a run that is still going, `cancel_run` with its `id`. What it already spent on finished
pictures stays spent; the rest comes back.

**One request, one `idempotencyKey`.** If a call times out or its answer is lost, call again with
the SAME key: you get the first answer back and nothing is spent twice. A new key (or none) makes
a second run and spends again. Never call again while a run is still going.

## Make a post

Daily posts come from the brand's own templates, drawn with its approved logo, colors and fonts.

- `render_template` with `slug` and `template` (`promotion`, `hours`, `menu`, `pix`,
  `new-product`, `status-offer` or `carousel`), plus `size` (`ig-post` 1080x1350, `ig-square`,
  `ig-story`, `wa-status` or `share-card`) and `text` for the template's words. It answers with a
  picture link that expires (`expiresAt`). Nothing is saved.
- The owner's saved posts: `list_designs` (with `brand` to filter), then `render_design` with the
  design's `id` (and `page` for a carousel) for a PNG or JPEG of it. Editing a post is the studio's
  job: send the owner there.

## Undo a version

`restore_version` with `slug`, `version` and the draft's `draftRev` brings an older version back
through the same approval rules. Read its outcome: `proposed` waits for the owner; `approving`
means an owner-authorized publishing key started a new version, whose run you follow. It never
changes the old version. Do not send another approval to force a proposal through.

## Bring a brand from a folder

A whole folder or zip of brand files (logos, icons, fonts, a guidelines PDF) is sorted into the
right places by `npx ideare import <folder|zip>` or the studio's folder door. Both show where each
file goes before anything changes. Over MCP, `get_folder_import` reads such a run and
`apply_import` uses it once the owner agrees with the review.

## Errors

Errors come as `{"error": {"code", "message", "details"}}`. Read the message before you retry.

| Code                  | What to do                                                                                    |
| --------------------- | --------------------------------------------------------------------------------------------- |
| `VALIDATION_ERROR`    | Fix the fields `details` names. An incomplete brand lists each one.                           |
| `NOT_FOUND`           | The slug, run or file isn't in this workspace, or doesn't exist. Check it with `list_brands`. |
| `CONFLICT`            | The draft moved on (`details` has it), the version is still being drawn, or nothing changed.  |
| `FORBIDDEN`           | This key can't do that. A read-only key (every key on the free plan) can only read.           |
| `PAYMENT_REQUIRED`    | Not enough credits. Tell the user; they can buy a pack or wait for the new month.             |
| `RATE_LIMIT_EXCEEDED` | Wait `details.retryAfterSecs`, then retry.                                                    |
| `QUOTA_EXCEEDED`      | A daily allowance is used up. It comes back at midnight; `details.retryAfterSecs` says when.  |
| `SERVICE_UNAVAILABLE` | AI or storage is paused or busy. Wait `details.retryAfterSecs`; nothing was charged.          |
| `NOT_IMPLEMENTED`     | That part isn't built yet. Don't retry.                                                       |

## Limits

- 120 tool calls a minute per key.
- Text suggestions, link imports and handle checks have daily allowances by plan; `get_usage`
  shows them.

## Signing in

Clients that support MCP sign-in open ideare's own page: the user checks the app's name and
presses Allow. That makes an API key named after the app, which the user can revoke in the
studio, under Keys. Such a key never publishes: its approvals are always proposals.

A user can also make a key in the studio, under Keys, and give it to the agent. Send it as
`Authorization: Bearer ideare_...` to `https://api.ideare.app/mcp`. In Claude Code:

```sh
claude mcp add --transport http ideare https://api.ideare.app/mcp --header "Authorization: Bearer $IDEARE_API_KEY"
```

## Without MCP

The same operations are REST routes on `https://api.ideare.app/v1`, with the same key, and
`@ideare/sdk` wraps them. The calls that take an `idempotencyKey` over MCP take an
`Idempotency-Key` header here.

| MCP tool           | REST                                                                 |
| ------------------ | -------------------------------------------------------------------- |
| `list_brands`      | `GET /v1/brands`                                                     |
| `get_brand`        | `GET /v1/brands/{slug}`                                              |
| `create_brand`     | `POST /v1/brands`                                                    |
| `update_draft`     | `PUT /v1/brands/{slug}/draft`                                        |
| `check_brand`      | `POST /v1/brands/{slug}/check`                                       |
| `approve_draft`    | `POST /v1/brands/{slug}/approve`                                     |
| `list_files`       | `GET /v1/brands/{slug}/files`                                        |
| `get_version`      | `GET /v1/brands/{slug}/versions/{n\|latest}` (no key)                |
| `get_run`          | `GET /v1/runs/{id}`, or `/v1/runs/{id}/events` as Server-Sent Events |
| `generate_symbols` | `POST /v1/brands/{slug}/symbols`                                     |
| `generate_art`     | `POST /v1/brands/{slug}/art`                                         |
| `generate_text`    | `POST /v1/ai/text`                                                   |
| `check_names`      | `POST /v1/names/check`                                               |
| `get_usage`        | `GET /v1/usage`                                                      |
| `import_brand`     | `POST /v1/imports/brand`                                             |
| `read_repo`        | `POST /v1/imports/repo`                                              |
| `get_folder_import`| `GET /v1/imports/folder/{runId}`                                      |
| `apply_import`     | `POST /v1/imports/folder/{runId}/apply`                               |
| `cancel_run`       | `DELETE /v1/runs/{id}`                                               |
| `restore_version`  | `POST /v1/brands/{slug}/versions/{version}/restore`                  |
| `render_template`  | `POST /v1/brands/{slug}/render`                                      |
| `list_designs`     | `GET /v1/designs`                                                    |
| `render_design`    | `POST /v1/designs/{id}/render`                                       |

Success answers are `{"data": ...}`. The full reference is at `https://api.ideare.app/openapi.json`.

## Never

- Never tell the user a change is live when `approve_draft` answered `proposed`.
- Never call `approve_draft` again to push a proposal through.
- Never edit a brand file in a project by hand: change the brand, approve it, then `ideare pull`.
- Never retry a spending call with a new `idempotencyKey`, and never loop AI calls for
  variations the user didn't ask for.
- Never redraw, recolor or stretch the logo yourself: use the files as they are.
- Never print, log or commit the `ideare_` key.
