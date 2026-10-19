# Testing the pncp.dev plugin

How to try every part of this plugin, written for store reviewers and anyone else.

## The test account

Store reviewers get an email and password in the submission form. It signs in with no second step.

The account is on the free plan: 100,000 requests a month and no credits. PNCP's data is public,
so it sees the same tenders and contracts as any other account. Of the account itself, an app sees
only its usage, quota and credits, never the email or payment data.

## Sign in

1. Install the plugin (see [README.md](README.md)).
2. Claude Code: type `/mcp`, pick pncp, choose Authenticate. Codex: `codex mcp login pncp` (Codex
   0.147 or later). ChatGPT and claude.ai: add the connector, then press Connect.
3. pncp.dev opens in your browser, in Portuguese. Press "Entrar com senha" (sign in with a
   password), then sign in with the test account. You do not need access to its inbox.
4. The next page says "Conectar" and the app's name. Check the address under "Volta para", where
   the app gets its answer, then press "Conectar".

The app gets its own API key, named after the app. To disconnect, revoke that key under
[Chaves](https://pncp.dev/app/chaves).

## Should work

The dates are fixed so the answers can be checked. The totals are what PNCP reported on
2026-10-19. PNCP keeps adding late records, so they can grow a little.

| Ask                                                                                                        | What happens                                                                                                                                                                                                                           |
| ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "List the pregão eletrônico tenders published on PNCP between October 12 and 18, 2026. Show the first 10." | Calls `get_pncp` on `/api/consulta/v1/contratacoes/publicacao` with those dates, `codigoModalidadeContratacao=6` and `tamanhoPagina=10`. Shows 10 tenders with what is being bought, the agency and the estimated value, out of 6,536. |
| "Which pregão eletrônico tenders are still open for proposals until December 18, 2026?"                    | Calls `get_pncp` on `/api/consulta/v1/contratacoes/proposta` with `dataFinal=20261218`. Shows 10 open tenders with their proposal deadline, out of 16,448.                                                                             |
| "Which contracts were signed between October 12 and 18, 2026, with whom, and for how much?"                | Calls `get_pncp` on `/api/consulta/v1/contratos` with those dates. Shows 10 contracts with the supplier, the value and when the term ends, out of 35,588.                                                                              |
| "Show me purchase 22/2026 of the agency with CNPJ 75.924.290/0001-69."                                     | Calls `get_pncp` on `/api/consulta/v1/orgaos/75924290000169/compras/2026/22`. Shows one purchase by the Município de Pérola d'Oeste (PR): a baler, a mower and more, with its values, modality and status.                             |
| "How much of my pncp.dev quota is left this month?"                                                        | Calls `get_usage`, which is free and makes no PNCP call. Shows the month, the calls per key, the total, the limit of 100,000 and the credit balance.                                                                                   |

## Should not work

| Ask                                                                  | What happens                                                                                                                                                    |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Buy more pncp.dev credits for me." or "Upgrade me to the Pro plan." | No tool buys or changes anything. The agent says so and points to https://pncp.dev/app/plano.                                                                   |
| "Use get_pncp to fetch https://example.com/api/test."                | `get_pncp` refuses it with `INVALID_PATH` before anything reaches PNCP, and it uses no quota. A path with `api_key=` or a `#` fragment is refused the same way. |
| "Publish a new tender on PNCP for my agency."                        | Not possible: the tools only read public `/api/` routes, and pncp.dev never passes on a gov.br login. The agent declines.                                       |

## What each tool can change

Every tool says what it does through `readOnlyHint`, `destructiveHint` and `openWorldHint`.

- `get_pncp` reads one page of a public PNCP `/api/` route, with GET. It changes nothing on PNCP.
  It uses one request of the month's quota, also when the answer comes from pncp.dev's cache, so
  it is read-only but not free. It reaches PNCP, so `openWorldHint` is true.
- `get_usage` reads the account's usage, quota and credits. It is free and reaches nothing outside
  pncp.dev.

Neither tool can buy credits, change the plan, or create, list or revoke keys. Only a person signed
in at pncp.dev can.
