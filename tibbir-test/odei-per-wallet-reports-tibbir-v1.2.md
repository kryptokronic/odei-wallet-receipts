# ODEI Per-Wallet Reports — TIBBIR Base Provenance Test

**Report version:** v1.2  
**Run date:** 2026-10-28 UTC  
**Network:** Base  
**Target token:** TIBBIR  
**Token contract:** `0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00`  
**Research modes:** Launch Provenance + Claim Audit + partial Wallet Analytics  
**Primary source ledger:** `odei-source-ledger-tibbir-v1.2.md`

---

## Scope Note

No wallet address was supplied directly. Two addresses were derived from TIBBIR launch evidence:

1. `0xdb2eae229527135787c8cca1efa9e14888ffc398` — launch transaction sender.
2. `0x4213c040d6c82a64951f8d0b3721073eb1f9313e` — initial allocation recipient.

These are **not canonical “creator” or “dev” labels**. The first is a launch-sender candidate; the second is an initial-allocation recipient. Real-world ownership attribution is not testable under the on-chain-only framework.

The January 2025 launch evidence requires an explicit provenance lookback of approximately 730 days. It must not be used to pass a default 180-day wallet-analysis gate.

---

# Wallet 1 — `0xdb2e…c398`

## 0. Completeness and Resolution

| Field | Status | Result |
|---|---|---|
| Address resolution | PARTIAL | Derived from the initial launch/mint transaction |
| Resolved role | YES | `launch_transaction_sender` |
| Contract deployer status | UNAVAILABLE | Contract-deployment evidence was not established |
| Creator status | NOT_TESTABLE | Launch sender is not automatically creator |
| Surf entity label | NO_ACTIVITY_FOUND | No label returned for the wallet |
| Base balance | YES | Approximately $2.05 in the chain-specific detail response |
| All-EVM balance | SECONDARY CONTEXT | Approximately $10.07; not Base-only |
| Base transfers endpoint | NO_ACTIVITY_FOUND / CONFLICT | Empty response conflicted with SQL evidence |
| EVM wallet history | PARTIAL | 16 pages reached the January 2025 launch period |
| Net worth | PARTIAL | Recent aggregate EVM series only; not a 730-day Base series |
| DeFi | YES | No positions returned |
| Hyperliquid | YES | Zero account value and no positions |
| Launch provenance | YES | Direct launch transaction evidence |
| Full trading score | INSUFFICIENT | Complete multi-token performance was not established |

**Relevant sources:** S008, S009, S010–S017, S024–S032.

## 1. Classification

**Working category:** Unknown — launch transaction sender candidate  
**Resolution confidence:** High for launch-sender role; low for creator or ownership role  
**Surf labels:** None returned

The wallet initiated the transaction that produced the initial TIBBIR mint events and targeted the Virtuals bonding proxy. That confirms a direct launch association. It does not prove that the wallet deployed the token contract, owned the project, or belonged to any named person.

## 2. Holdings and Net Worth

### Chain-specific Base snapshot

- Reported Base balance: approximately **$2.05**.
- Current TIBBIR balance: not returned for the Base wallet detail snapshot.

### Aggregate EVM context

The wallet-detail and net-worth endpoints returned broader EVM data:

- Aggregate EVM balance: approximately **$10.07**.
- Recent returned net-worth range: approximately **$9.36–$10.60**.
- This is not a complete 730-day trend and must not be presented as Base-only net worth.

## 3. Activity Profile

The wallet-history endpoint returned 16 pages of 100 records and reached a timestamp before the January 2025 launch period. The history endpoint was therefore useful for temporal coverage, but the returned rows did not provide a complete token-level trade ledger for the full wallet.

### Verified launch-period DEX activity

Window: 2025-01-12 through 2025-01-19 UTC  
Asset: TIBBIR on Base

| Metric | Result |
|---|---:|
| Distinct TIBBIR trade transactions | 74 |
| Buy-side trade rows | 51 |
| Sell-side trade rows | 29 |
| TIBBIR bought | 81.10M |
| TIBBIR sold | 79.91M |
| Buy-side one-sided DEX value | $103.6K |
| Sell-side one-sided DEX value | $112.5K |
| Combined observed one-sided notional | $216.1K |

The DEX table’s `amount_usd` is one-sided token-sold value. The $216.1K figure is not gross two-sided volume and is not realized PnL.

## 4. Trading Performance

| Asset | Chain | First observed trade | Buy rows | Sell rows | Observed one-sided notional | Status |
|---|---|---|---:|---:|---:|---|
| TIBBIR | Base | 2025-01-12 00:35 UTC | 51 | 29 | $216.1K | Partial |

The first observed TIBBIR DEX activity occurred roughly five minutes after the initial mint transaction at 2025-01-12 00:30 UTC.

Unavailable or incomplete:

- complete top-ten token ranking;
- complete mature-buy denominator;
- +7-day and +30-day BTC-relative returns;
- FIFO-matched closed-lot PnL;
- complete cash-flow PnL;
- hold-time distribution;
- full wallet-level trade universe.

## 5. Smart Money Score

| Component | Result | Points |
|---|---|---:|
| Timing edge | Full 30-day BTC-relative history unavailable | NA |
| Hit rate | Complete mature-buy denominator unavailable | NA |
| PnL | Complete buy/sell coverage unavailable | NA |
| Consistency | Both lookback halves not fully analyzed | NA |
| Behaviour quality | Launch-linked activity observed; no complete risk screen | NA |

```text
Smart Money Score: NA
Band: INSUFFICIENT
```

The wallet must not be classified as Smart Money, Skilled, Average, or No edge from this run.

## 6. Behavioural Patterns

| Pattern | Tier | Count | Finding |
|---|---|---:|---|
| Launch-linked TIBBIR trading | Pattern | 74 transactions | Wallet initiated launch transaction and traded TIBBIR repeatedly during the launch period |
| Virtuals bonding-proxy interaction | Confirmed | 1 | Initial launch transaction targeted the labeled Virtuals bonding proxy |
| Uniswap pool interaction | Pattern | Multiple | Wallet traded against the labeled Uniswap V2 pool |
| Wash trading | Not established | — | Repeated buys and sells are insufficient proof |
| Insider timing | Not established | — | Launch proximity is notable but not an identity or intent proof |
| Current accumulation | Unavailable | — | Complete 7-day and 30-day flow was not calculated |

## 7. Connected Addresses

| Address | Label | Role | Evidence tier | Link |
|---|---|---|---|---|
| `0xf66dea…3259` | Virtuals Protocol — Bonding (Proxy) | Launchpad/protocol target | Confirmed | Initial mint transaction |
| `0xa4a2e2…c6e00` | Ribbita by Virtuals — TIBBIR | Token contract | Confirmed | Mint and trade events |
| `0x0c3b46…4888` | Uniswap — V2 Pool | Pool counterparty | Confirmed | TIBBIR trade events |
| `0x6b2c0c…4d58` | DEX Router — OKX | Router | Confirmed | Later trade transaction |

First-ever funder, top counterparties by USD/count, and shared-funder analysis were not completed and remain `UNAVAILABLE`.

## 8. DeFi and Hyperliquid Risk

- DeFi positions: none returned.
- Hyperliquid account: zero value, no open positions, no reported balances.
- Liquidation risk: no active position returned.

## 9. Opportunities and Watch Triggers

No current TIBBIR accumulation lead was confirmed.

The wallet is better treated as a **historical provenance lead** than as a current accumulation wallet.

Re-check if:

- the wallet resumes material TIBBIR buying;
- the wallet receives a new Surf label;
- the wallet transfers to or from a publicly labeled project entity;
- a complete trade ledger becomes available.

## 10. Risks and Red Flags

- Launch sender is not necessarily contract deployer or creator.
- Current holdings are negligible.
- The wallet-transfer endpoint conflicted with SQL-derived activity.
- Rapid launch-period activity requires further counterparty and price-path analysis before any wash-trading conclusion.
- No permitted evidence binds this wallet to a named individual.

## 11. Verdict and Logging

`0xdb2e…c398` is directly associated with TIBBIR’s launch transaction and early DEX trading. The strongest defensible role is **launch transaction sender**. The available evidence does not prove that it deployed the contract, owned the project, or belonged to Micky Malka. Wallet analytics are incomplete, and the Smart Money Score is insufficient.

**Decision:** Monitor as a provenance lead; do not treat as a validated Smart Money wallet.

```csv
2026-10-28,0xdb2eae229527135787c8cca1efa9e14888ffc398,base,launch_transaction_sender_candidate,NA,INSUFFICIENT,none,Monitor,"Launch and early TIBBIR activity confirmed; creator and person ownership not established; wallet analytics incomplete"
```

---

# Wallet 2 — `0x4213…313e`

## 0. Completeness and Resolution

| Field | Status | Result |
|---|---|---|
| Address resolution | YES | Derived from initial mint recipient field |
| Resolved role | YES | `initial_allocation_recipient` |
| Dev-wallet status | NOT_TESTABLE | No explicit dev/team label returned |
| Surf entity label | NO_ACTIVITY_FOUND | No label returned |
| Current Base balance | YES | Approximately $0.047 |
| Current TIBBIR balance | YES | Approximately 0.2178 TIBBIR |
| Transfer endpoint | NO_ACTIVITY_FOUND | Empty inbound and outbound responses |
| Wallet history | PARTIAL | First page returned with more data available |
| Net worth | PARTIAL | Recent aggregate EVM series only |
| DEX performance | UNAVAILABLE | No complete wallet-level DEX universe established |
| Smart Money Score | INSUFFICIENT | Hard gates and core performance data unavailable |

**Relevant sources:** S008, S018–S023, S024.

## 1. Classification

**Working category:** Unknown — initial allocation recipient  
**Resolution confidence:** High for allocation recipient role; low for team or dev role  
**Surf labels:** None returned

The wallet received 875,870,016 TIBBIR in the initial mint transaction. That is a confirmed allocation relationship, not proof of project-team status or personal ownership.

## 2. Holdings and Net Worth

- Current Base wallet value: approximately **$0.047**.
- Current TIBBIR: approximately **0.2178 TIBBIR**.
- Recent returned net-worth range: approximately **$0.0466–$0.0491**.
- The net-worth series is a recent aggregate snapshot, not a complete historical allocation-distribution curve.

## 3. Activity Profile

The wallet-history endpoint returned a first page with more history available. The returned history included the initial launch transaction and later activity, but a complete token-level activity reconstruction was not completed.

The transfer endpoint returned empty inbound and outbound responses. This should not be interpreted as proof of no historical activity because the initial mint is directly visible in SQL and wallet history.

## 4. Trading Performance

No complete wallet-level DEX trade dataset was established for this address.

```text
Trading performance: UNAVAILABLE
Closed-lot PnL: UNAVAILABLE
BTC-relative returns: UNAVAILABLE
```

## 5. Smart Money Score

```text
Smart Money Score: NA
Band: INSUFFICIENT
```

The address cannot be scored because current scale is negligible and the complete mature-buy, multi-token, PnL, and return datasets were not established.

## 6. Behavioural Patterns

| Pattern | Tier | Count | Finding |
|---|---|---:|---|
| Initial TIBBIR allocation | Confirmed | 1 | Received 875.87M TIBBIR in the launch mint transaction |
| Current material holding | Not present | — | Current balance is approximately 0.2178 TIBBIR |
| Distribution history | Unavailable | — | Complete token transfer history not reconstructed |
| Current accumulation | Unavailable | — | 7-day and 30-day net flow not calculated |

## 7. Connected Addresses

| Address | Label | Role | Evidence tier | Link |
|---|---|---|---|---|
| `0xdb2eae…c398` | No label | Initial launch transaction sender | Confirmed | Same launch transaction |
| `0xf66dea…3259` | Virtuals Protocol — Bonding (Proxy) | Launchpad/protocol target | Confirmed | Same launch transaction |
| `0xa4a2e2…c6e00` | Ribbita by Virtuals — TIBBIR | Token contract | Confirmed | Initial mint recipient relationship |

First funder, top counterparties, shared-funder analysis, and sweep destinations are `UNAVAILABLE`.

## 8. DeFi and Hyperliquid Risk

No complete DeFi or Hyperliquid analysis was performed for this secondary allocation address.

## 9. Opportunities and Watch Triggers

No current accumulation lead was confirmed. The wallet holds only a negligible current TIBBIR balance.

Re-check if:

- material TIBBIR is received or moved;
- a Surf label is added;
- the allocation address is explicitly labeled by the protocol or token project;
- full historical transfers become available.

## 10. Risks and Red Flags

- Initial allocation does not prove team, dev, treasury, or personal ownership.
- The wallet is currently economically immaterial.
- Historical distribution and counterparty analysis remain incomplete.
- No permitted evidence binds the wallet to Micky Malka or any other individual.

## 11. Verdict and Logging

`0x4213…313e` is a confirmed initial-allocation recipient for TIBBIR. It should not be called a dev wallet or creator wallet without additional explicit evidence. Its current holdings are negligible, and it does not qualify for a Smart Money Score.

**Decision:** Monitor only as a historical allocation address; do not add as a Smart Money wallet.

```csv
2026-10-28,0x4213c040d6c82a64951f8d0b3721073eb1f9313e,base,initial_allocation_recipient,NA,INSUFFICIENT,none,Monitor,"Initial TIBBIR allocation confirmed; dev/team and person ownership not established; current holdings negligible"
```

---

## Claim Audit Summary

| Claim | Result | Evidence | Limitation |
|---|---|---|---|
| `0xdb2e…c398` initiated TIBBIR launch | CONFIRMED | Initial launch transaction | Does not prove creator or ownership |
| `0x4213…313e` received initial allocation | CONFIRMED | Mint event in same transaction | Does not prove dev/team role |
| `0xdb2e…c398` is the contract deployer | NOT_ESTABLISHED | No deployment evidence in this run | Launch caller may differ from deployer |
| `0xdb2e…c398` is a creator wallet | NOT_ESTABLISHED | No explicit creator field | Role terminology must remain narrow |
| Either wallet belongs to Micky Malka | IDENTITY_NOT_TESTABLE | No Surf label or cryptographic attestation | No deanonymization permitted |
| TIBBIR is directly associated with Virtuals Protocol | CONFIRMED | Labeled bonding proxy and contract association | Protocol association is not ownership |
