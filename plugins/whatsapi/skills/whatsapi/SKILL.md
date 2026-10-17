---
name: whatsapi
description: "Send WhatsApp messages from the user's own numbers, read and answer their chats, send sign-in codes and pair numbers, with whatsapi.sh over its MCP tools. Use when the user asks to message someone on WhatsApp, read or answer a WhatsApp chat, send or check a verification code, check whether a phone is on WhatsApp, or link a WhatsApp number. Requires the whatsapi MCP server (setup guide: https://docs.whatsapi.sh/en/mcp)."
---

# whatsapi.sh workflows

whatsapi.sh links the user's own WhatsApp numbers as linked devices, the way WhatsApp Web does:
the phone keeps working. It is not the official WhatsApp Business API, so WhatsApp can restrict a
number that sends like a machine. The tools are built to stop that from happening. Work with them.

Three facts shape every call:

- **Most sends wait in a queue.** A message to someone who hasn't written to this number in the
  last 24 hours comes back with `status: "queued"` and a `scheduledAt`, not `"sent"`. Queued
  messages leave one at a time, 15 to 25 minutes apart. Tell the user it is queued and roughly
  when it leaves. A reply to someone who wrote in the last 24 hours goes out now, and so does a
  message to a group.
- **Every send costs one message** of the monthly quota, charged when it is accepted. `get_usage`
  shows what is left (`monthUsed`, `monthLimit`, `dayUsed`, `dayLimit`, `sendsPerMinute`).
- **A sent message can't be taken back.** Before you send anything the user didn't dictate word
  for word, show them the text and the recipient and wait for a yes.

## Before the first send

1. `list_numbers`. A number must be `connected` to send. With none, offer to add one (see "Pair a
   number"). `disconnected` means pair it again. `banned` means stop (see "Restricted numbers").
2. With more than one connected number, ask which one sends, and pass its id or its phone as
   `from`. With one, leave `from` out.

## Send a message

1. `send_message` with `to`, `text` and an `idempotencyKey` you make up (a new UUID). `to` is a
   phone in international format (`+5511988887777`) or an address from a chat or webhook
   (`…@s.whatsapp.net`, `…@lid`, or `…@g.us` for a group).
2. Read the answer: `status` (`queued` or `sent`), `scheduledAt`, `id`, `quotaRemaining` and
   `newConversationsRemaining`.
3. While a message is queued, `list_queued_messages` shows it, and `cancel_queued_message` with
   its `id` removes it before it leaves. The answer says whether the quota came back.

Other sends take the same `to`, `from` and `idempotencyKey`:

- `send_media`: `type` (`image`, `video`, `audio`, `document`) and `url` (best) or `base64` with
  `mimeType`. `caption` for an image or video, `fileName` for a document. ogg/opus audio becomes a
  voice note. Files are limited to 16 MB.
- `send_location`: `latitude`, `longitude`, optional `name`.
- `send_contact`: `name` and `vcard`.
- `send_batch`: one `text` to up to 25 recipients (`to` is a list). It needs a paid plan. Every
  recipient waits the full gap, even known contacts, and each costs one message.

`skipQueue: true` sends at once. Use it only when the recipient is waiting for that message right
now, such as a confirmation they just asked for. Never use it to go faster.

**One send, one `idempotencyKey`.** If a send times out or its answer is lost, call it again with
the SAME key: it runs once and returns the first answer. A new key sends a second message. Keys
are kept for 24 hours.

## Read and answer a chat

1. `list_chats` (optional `number`, `limit` up to 500): the chats a number kept, most recent
   first.
2. `get_chat_history` with `chat` (a phone in international format, or the `…@g.us` or `…@lid`
   address `list_chats` gave) and optional `number` and `limit` (up to 100). Newest first.
3. To answer, `send_message` with `to` set to that chat.

`typing` shows "typing…" in a chat (free, clears on its own after a few seconds). `mark_read` with
`to` and `messageIds` puts blue ticks on received messages. The other person sees them, so do it
only when the user wants it.

## Sign-in codes

- `send_otp` with `to` (optional `template` containing `{code}`, and `expiresInSeconds`, 300 by
  default). It sends a 6-digit code and returns it. It never waits in the queue and costs one
  message. One number can get a new code once a minute.
- `check_otp` with `to` and `code` consumes the code. A wrong or expired code is the error
  `OTP_INVALID`, never a "false". Five wrong guesses kill the code.

## Check a phone

`check_number` with `phone` (`+5511988887777`) says whether it has WhatsApp, and which form matched
(Brazilian mobiles are tried with and without the extra 9). `verified: false` means WhatsApp
couldn't be reached and the answer assumed yes. Free.

## Pair a number

1. `create_number` with `name` (a label only the user sees) and `age`: how long the line has
   really been in use, `new`, `weeks` or `established`. Ask the user. It sets how many new
   conversations the number may start a day, 5 when new up to 20 when established. When unsure,
   leave the default, `new`.
2. `pair_number` with `numberId`. It answers with a QR code image: show it, and tell the user to
   scan it in WhatsApp, Settings, Linked devices. With `mode: "code"` and `phone`, it answers with
   an 8-character code to type there instead.
3. Call `pair_number` again every few seconds while they scan. The QR changes every 20 seconds, so
   always show the newest one. `state` becomes `connected` when the scan lands. When `expiresIn`
   reaches 0, call it again to start over.

## Restricted numbers

`number_status` with `numberId` answers `connected`, `pairing`, `disconnected` or `banned`. For
`banned`, stop sending from that number. Tell the user to open WhatsApp on the phone and follow
the notice there: a restriction often lifts within an hour, and can take 24 hours. Only after they
say WhatsApp works on the phone, call `pair_number` with `recoveryConfirmed: true`. Never set it
on your own.

## Sending safely

- Message people who expect to hear from the user, during waking hours where they live.
- Vary the wording between recipients. Don't open a message to a stranger with a link.
- Each number has a daily budget of new conversations (people it never talked to). When it runs
  out, sends to new people fail with `QUOTA_EXCEEDED` and `details.scope: "newConversations"`
  until midnight. A reply never spends it. More numbers bring more budget; waiting is the only
  other fix.

## Webhooks

`get_webhook` shows where events go. `set_webhook` with `url` (https) and optional `events` starts
them. The answer carries the signing secret ONCE, on the first registration: hand it to the user
to store, and don't repeat it anywhere else. `test_webhook` sends a `ping` and reports what the
server answered. `get_supabase_hook` and `set_supabase_hook` send a Supabase project's phone codes
over WhatsApp; that secret also comes back once.

## Errors

An error comes back with `isError: true` and `{ "error": { "code", "message", "details" } }`. When
waiting fixes it, `details.retryAfterSecs` says how long. Act on the code:

| Code                     | What to do                                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `UNAUTHORIZED`           | The sign-in or key is missing or revoked. Ask the user to sign in again. Do not retry.                                   |
| `NUMBER_NOT_CONNECTED`   | No usable number. Run `list_numbers`, then pair one or ask the user to check WhatsApp on the phone. Retrying won't help. |
| `NOT_FOUND`              | Wrong number id or message id. Run `list_numbers` or `list_queued_messages`.                                             |
| `VALIDATION_ERROR`       | A field is wrong; `details` says which. Fix it and call again.                                                           |
| `CONFLICT`               | A send with this `idempotencyKey` is still running: wait `details.retryAfterSecs`, then repeat with the same key.        |
| `IDEMPOTENCY_KEY_REUSED` | That key was used for a different request. Make a new one.                                                               |
| `RATE_LIMIT_EXCEEDED`    | Too fast. Wait `details.retryAfterSecs`, then retry once.                                                                |
| `QUOTA_EXCEEDED`         | `details.scope` says which limit: `day`, `month` or `newConversations`. Tell the user when it clears (`resetAt`).        |
| `PAYMENT_REQUIRED`       | Only a different plan lifts it (more numbers, batch sends). Tell the user. Never retry.                                  |
| `OTP_INVALID`            | The code is wrong or expired. Say so; offer to send a new one.                                                           |
| `PAIRING_COOLDOWN`       | Too many pairing codes. Wait `details.retryAfterSecs`.                                                                   |
| `GATEWAY_TIMEOUT`        | WhatsApp didn't confirm in time. Read the chat before sending again, and if you do, use the same `idempotencyKey`.       |
| `GATEWAY_ERROR`          | WhatsApp refused it. Retry once.                                                                                         |
| `FORBIDDEN`              | The account is suspended. Tell the user.                                                                                 |

## Signing in

Claude, ChatGPT and other clients that support MCP sign-in need nothing from you: given
`https://api.whatsapi.sh/mcp`, they open whatsapi.sh and the user presses Connect there. In Codex,
the user runs `codex mcp login whatsapi` (Codex 0.147 or later). Either way whatsapi.sh makes a key
named after the app, which the user can revoke under API keys in the dashboard.

Where no browser can come back to you (a server, a container, an SSH session), sign in with a
code:

```sh
curl https://api.whatsapi.sh/oauth/device_authorization -d client_id=whatsapi-agent
```

Show the user the `verification_uri_complete` link from the answer. They open it on any device,
check the code and press Connect. Meanwhile, ask for the key every 5 seconds:

```sh
curl https://api.whatsapi.sh/oauth/token -d client_id=whatsapi-agent \
  -d grant_type=urn:ietf:params:oauth:grant-type:device_code -d device_code=DEVICE_CODE
```

`authorization_pending` means keep waiting. Then `access_token` is a `wa_` key, sent only once:
send it as `Authorization: Bearer wa_…` to `/mcp`. The code expires after 10 minutes.

## Never

- Never send a message the user hasn't approved.
- Never retry a send with a new `idempotencyKey`.
- Never use `skipQueue` or turn pacing off to send faster.
- Never set `recoveryConfirmed` on your own.
- Never print, log or commit a `wa_` key or a webhook secret.
