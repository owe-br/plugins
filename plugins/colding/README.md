# colding

Send and read email from mailboxes you connect to [colding](https://colding.app/en). Your agent
can warm them up, check addresses, manage contacts, run campaigns, read replies and answer them.
It can also send your app's receipts and sign-in links from a mailbox you keep for that.

## What's inside

- A [skill](skills/colding/SKILL.md) for email workflows, permissions, requests for a person's
  help, and safe retries.
- The remote MCP server at `https://api.colding.app/mcp`. The email tools run on colding's server.
- Plugin manifests and MCP connection settings.

Each connection belongs to one workspace. The owner chooses from seven permissions: Read,
Operate, Send outreach, Check addresses, Send app email, Manage agent inboxes and Set up the
workspace. Read is selected to start. The tools a connection can use depend on its permissions
and mailbox read list, not a fixed tool total.

Set up the workspace (`setup`) lets a key connect mailboxes by login, replace their logins,
confirm their addresses, manage tracking domains and set the postal address. It works across the
whole workspace, so it cannot have mailbox, read or campaign lists. It stops working if the
person who made the key is no longer the owner. With Read too, it can set up a webhook when none exists, or manage one
a key saved. A webhook a person saved stays with a person.

Microsoft and Google sign-in, disconnecting a mailbox, key changes, billing and accepting the
acceptable use policy still need a person. The skill explains how to open a request for them.

Agent inboxes and app email from colding's own servers are not on any plan for sale. The plugin
does not make them available. It does not attach files to outgoing email or provide a Python SDK.

## Connect and sign in

Add `https://api.colding.app/mcp` as a remote MCP server in your app. When it asks you to sign in,
check that the page is at `https://console.colding.app/auth/authorize`. Use your existing colding
account and pick a workspace you own. Check the app's name and return address, choose only the
permissions and limits it needs, then press Connect. Our team opens accounts by hand; public
sign-up is closed.

The app gets its own `cd_` API key. Find it in the console's API keys list at
[console.colding.app](https://console.colding.app). The workspace owner can change its limits or
revoke it there. No key belongs in this plugin's files.

On a machine with no browser, use the device code flow with `client_id=colding-cli`. Open
`https://console.colding.app/auth/device` on another device, check the code and approve it only
if you asked for the connection. The code expires in 10 minutes.

Client-specific plugin installation and sign-in have not been tested for this revision. See
[TESTING.md](TESTING.md) for the checks and the empty proof table. These instructions do not
promise that a client loads every tool or works with a full-permission key.

## Links

- [Docs](https://colding.app/en/docs)
- [Privacy](https://colding.app/en/privacy)
- [Terms](https://colding.app/en/terms)
- [Acceptable use policy](https://colding.app/en/aup)
- Help: [hello@colding.app](mailto:hello@colding.app)
- Privacy questions: [privacy@colding.app](mailto:privacy@colding.app)
