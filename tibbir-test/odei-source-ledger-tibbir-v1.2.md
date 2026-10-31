# ODEI Source Ledger — TIBBIR Base Test

**Ledger version:** v1.2  
**Run date:** 2026-10-28 UTC  
**Purpose:** Reproduce the TIBBIR launch-provenance and partial wallet-analysis run  
**Primary token:** TIBBIR on Base, `0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00`

---

## Ledger Conventions

- `YES` means the call returned usable data for the stated field.
- `PARTIAL` means some data returned but coverage was incomplete.
- `UNAVAILABLE` means failed, unsupported, rejected, or no usable result.
- `NO_ACTIVITY_FOUND` means a valid call returned empty data.
- External web searches are context-only and were not used as on-chain evidence.
- Provenance evidence was outside the default 180-day wallet-analysis window and therefore belongs to a separate historical provenance extension.

---

## A. Token and Project Resolution

### S001 — Project search

```text
Operation: search-project
Parameters: --q TIBBIR --limit 20 --json
Result: YES / empty catalog result
Status: NO_ACTIVITY_FOUND
Use: Project catalog did not return a dedicated TIBBIR project record.
```

### S002 — Exact token resolution

```text
Operation: search-token
Parameters: --q TIBBIR --chain base --limit 20 --json
Result: TIBBIR on Base
Contract: 0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00
Status: YES
Use: Canonical token/chain resolution.
```

### S003 — Fuzzy project detail

```text
Operation: project-detail
Parameters: --q TIBBIR --fields overview,contracts,token_info,team,tge_status --json
Result: Virtuals Protocol context with TIBBIR contract included
Status: PARTIAL
Use: Parent-protocol context only; not treated as TIBBIR-specific team ownership.
```

### S004 — Alternate fuzzy project detail

```text
Operation: project-detail
Parameters: --q Ribbita --fields overview,contracts,token_info,team,tge_status --json
Result: Upstream error after retries
Status: UNAVAILABLE
Use: Not used for conclusions.
```

---

## B. Catalog and Schema Discovery

### S005 — Catalog search

```text
Operation: surf catalog search
Parameters: "base transactions"; "base token transfers"; "base dex trades"
Result: base_transfers and base_dex_trades discovered
Status: YES
```

### S006 — Transfer table schema

```text
Operation: surf catalog show
Parameters: agent.base_transfers
Result: Schema and partition metadata
Key fields: block_date, block_time, tx_hash, tx_from, tx_to, from, to, contract_address, symbol, amount, amount_usd
Partition: toYYYYMM(block_date)
Status: YES
```

### S007 — DEX table schema

```text
Operation: surf catalog show
Parameters: agent.base_dex_trades
Result: Schema and partition metadata
Key fields: block_date, block_time, token_bought_address, token_sold_address, token_bought_amount, token_sold_amount, amount_usd, taker, tx_hash
Partition: toYYYYMM(block_date)
Important semantic: amount_usd is one-sided token-sold value.
Status: YES
```

---

## C. Initial Mint and Launch Provenance

### S008 — Rejected broad initial-mint preflight

```text
Operation: onchain-sql-preflight
Parameters: max_rows=1000
Table: agent.base_transfers
Window: block_date >= 2020-01-01
Filter: TIBBIR contract; from = zero address
Result: Rejected
Reason: Missing partition filter; window exceeded accepted range
Status: UNAVAILABLE / REJECTED
```

### S009 — Bounded initial-mint preflight

```text
Operation: onchain-sql-preflight
Parameters: max_rows=1000
Table: agent.base_transfers
Window: block_date >= 2024-10-28 AND block_date < 2025-10-28
Filter: contract_address = 0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00; from = zero address
Result: Accepted
Estimated scan: approximately 1.9M rows
Status: YES
```

### S010 — Initial-mint SQL execution

```sql
SELECT block_time, block_number, tx_hash, evt_index,
       `from`, `to`, amount, amount_usd, tx_from, tx_to
FROM agent.base_transfers
WHERE contract_address = '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00'
  AND block_date >= toDate('2024-10-28')
  AND block_date < toDate('2025-10-28')
  AND `from` = '0x0000000000000000000000000000000000000000'
ORDER BY block_time ASC
LIMIT 20
```

Result:

- `2025-01-12 00:30:03 UTC`;
- transaction `0x6a56599bb11f22a1de165dd4a9887724188098527b230fb8e018d6bb3474f71e`;
- `124,129,984` TIBBIR minted to the token contract;
- `875,870,016` TIBBIR minted to `0x4213c040d6c82a64951f8d0b3721073eb1f9313e`;
- `tx_from = 0xdb2eae229527135787c8cca1efa9e14888ffc398`.

Status: YES for first observed mint within the validated coverage window.

### S011 — Launch transaction detail

```text
Operation: onchain-tx
Parameters: --chain base --hash 0x6a56599bb11f22a1de165dd4a9887724188098527b230fb8e018d6bb3474f71e --include labels --json
Result:
- from = 0xdb2eae229527135787c8cca1efa9e14888ffc398
- to = 0xf66dea7b3e897cd44a5a231c61b6b4423d613259
- target label = Virtuals Protocol / Bonding (Proxy)
Status: YES
Use: Confirms launch transaction sender and protocol target; does not prove contract deployment or human ownership.
```

---

## D. Primary Wallet — `0xdb2e…c398`

### S012 — Wallet detail

```text
Operation: wallet-detail
Parameters: --address 0xdb2eae229527135787c8cca1efa9e14888ffc398 --chain base --fields balance,tokens,labels,nft --json
Result:
- Base chain balance approximately $2.05
- Aggregate EVM value approximately $10.07
- No TIBBIR returned in the Base token list
- labels field reported an upstream error in the detail response
Status: PARTIAL
```

### S013 — Wallet labels

```text
Operation: wallet-labels-batch
Parameters: --addresses 0xdb2eae229527135787c8cca1efa9e14888ffc398 --json
Result: empty label array
Status: NO_ACTIVITY_FOUND / no label returned
```

### S014 — Wallet transfers inbound

```text
Operation: wallet-transfers
Parameters: --address 0xdb2eae229527135787c8cca1efa9e14888ffc398 --chain base --flow in --limit 100 --offset 0 --include labels --json
Result: empty data
Status: NO_ACTIVITY_FOUND at endpoint level; reconciled against SQL as PARTIAL
```

### S015 — Wallet transfers outbound

```text
Operation: wallet-transfers
Parameters: --address 0xdb2eae229527135787c8cca1efa9e14888ffc398 --chain base --flow out --limit 100 --offset 0 --include labels --json
Result: empty data
Status: NO_ACTIVITY_FOUND at endpoint level; reconciled against SQL as PARTIAL
```

### S016 — Wallet history pages 1–16

Common parameters:

```text
Operation: wallet-history
Address: 0xdb2eae229527135787c8cca1efa9e14888ffc398
Chain: base
Limit: 100
Sort: timestamp
Order: desc
Include: labels
```

Page boundaries:

| Page | `before` | First timestamp | Last timestamp | Rows | `has_more` |
|---:|---:|---:|---:|---:|---|
| 1 | omitted | 1783518445 | 1746696077 | 100 | true |
| 2 | 1746696077 | 1746438577 | 1739744923 | 100 | true |
| 3 | 1739744923 | 1739740217 | 1739235321 | 100 | true |
| 4 | 1739235321 | 1739235229 | 1738084401 | 100 | true |
| 5 | 1738084401 | 1738084329 | 1737797641 | 100 | true |
| 6 | 1737797641 | 1737774417 | 1737600777 | 100 | true |
| 7 | 1737600777 | 1737600765 | 1737495573 | 100 | true |
| 8 | 1737495573 | 1737495453 | 1737329045 | 100 | true |
| 9 | 1737329045 | 1737325661 | 1736990991 | 100 | true |
| 10 | 1736990991 | 1736990981 | 1736980701 | 100 | true |
| 11 | 1736980701 | 1736980691 | 1736887051 | 100 | true |
| 12 | 1736887051 | 1736887045 | 1736860255 | 100 | true |
| 13 | 1736860255 | 1736860165 | 1736807745 | 100 | true |
| 14 | 1736807745 | 1736807739 | 1736793561 | 100 | true |
| 15 | 1736793561 | 1736792415 | 1736669733 | 100 | true |
| 16 | 1736669733 | 1736660809 | 1736533833 | 100 | true |

Status: PARTIAL; history reached before the launch period but complete wallet-level token reconstruction was not completed.

### S017 — Net worth

```text
Operation: wallet-net-worth
Parameters: --address 0xdb2eae229527135787c8cca1efa9e14888ffc398 --json
Result: recent aggregate EVM series
Range returned: approximately $9.36–$10.60
Status: PARTIAL
Use: Secondary EVM context only; not Base-specific or a full 730-day trend.
```

### S018 — DeFi positions

```text
Operation: wallet-protocols
Parameters: --address 0xdb2eae229527135787c8cca1efa9e14888ffc398 --limit 100 --offset 0 --json
Result: empty positions
Status: YES / no positions returned
```

### S019 — Hyperliquid account

```text
Operation: hyperliquid-account
Parameters: --address 0xdb2eae229527135787c8cca1efa9e14888ffc398 --json
Result: total_value_usd = 0; no perp positions; no spot balances
Status: YES / no Hyperliquid activity found
```

---

## E. Secondary Wallet — `0x4213…313e`

### S020 — Wallet detail

```text
Operation: wallet-detail
Parameters: --address 0x4213c040d6c82a64951f8d0b3721073eb1f9313e --chain base --fields balance,tokens,labels,nft --json
Result:
- Base value approximately $0.0467
- TIBBIR balance approximately 0.2178
- labels field reported upstream error in detail response
Status: PARTIAL
```

### S021 — Wallet labels

```text
Operation: wallet-labels-batch
Parameters: --addresses 0x4213c040d6c82a64951f8d0b3721073eb1f9313e --json
Result: empty label array
Status: NO_ACTIVITY_FOUND / no label returned
```

### S022 — Wallet history

```text
Operation: wallet-history
Parameters: --address 0x4213c040d6c82a64951f8d0b3721073eb1f9313e --chain base --limit 100 --sort-by timestamp --order desc --include labels --json
Result: 100 rows; has_more=true; initial launch transaction visible
Status: PARTIAL
```

### S023 — Wallet transfers inbound

```text
Operation: wallet-transfers
Parameters: --address 0x4213c040d6c82a64951f8d0b3721073eb1f9313e --chain base --flow in --limit 100 --offset 0 --include labels --json
Result: empty data
Status: NO_ACTIVITY_FOUND at endpoint level; reconciled against SQL as PARTIAL
```

### S024 — Wallet transfers outbound

```text
Operation: wallet-transfers
Parameters: --address 0x4213c040d6c82a64951f8d0b3721073eb1f9313e --chain base --flow out --limit 100 --offset 0 --include labels --json
Result: empty data
Status: NO_ACTIVITY_FOUND at endpoint level; reconciled against SQL as PARTIAL
```

### S025 — Net worth

```text
Operation: wallet-net-worth
Parameters: --address 0x4213c040d6c82a64951f8d0b3721073eb1f9313e --json
Result: recent aggregate series approximately $0.0466–$0.0491
Status: PARTIAL
```

---

## F. Material Address Label Batch

### S026 — Label batch

```text
Operation: wallet-labels-batch
Parameters:
--addresses 0xdb2eae229527135787c8cca1efa9e14888ffc398,
0x4213c040d6c82a64951f8d0b3721073eb1f9313e,
0xf66dea7b3e897cd44a5a231c61b6b4423d613259,
0x0c3b466104545efa096b8f944c1e524e1d0d4888,
0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00
--json
```

Returned labels:

- `0xf66dea…3259`: Virtuals Protocol — Bonding (Proxy)
- `0x0c3b46…4888`: Uniswap — V2 Pool
- `0xa4a2e2…c6e00`: Ribbita by Virtuals — TIBBIR
- no labels for `0xdb2e…c398` or `0x4213…313e`

Status: YES for material address labels.

---

## G. Launch-Window Transfer Query

### S027 — Launch-window transfer preflight

```text
Operation: onchain-sql-preflight
Table: agent.base_transfers
Window: 2025-01-10 through 2025-01-15
Addresses: 0xdb2e…c398 and 0x4213…313e
Branches: incoming and outgoing UNION ALL
Result: accepted
Status: YES
```

### S028 — Launch-window transfer execution

```text
Operation: onchain-sql
Table: agent.base_transfers
Window: 2025-01-10 through 2025-01-15
Addresses: 0xdb2e…c398 and 0x4213…313e
Result: 545 rows returned before output truncation
Status: PARTIAL for broad transfer listing
Use: Direct launch/transfer relationship only; not a complete counterparty analysis.
```

---

## H. TIBBIR Launch-Period DEX Aggregates

### S029 — Broad DEX preflight rejected

```text
Operation: onchain-sql-preflight
Table: agent.base_dex_trades
Window: 2025-01-01 through 2025-12-30
Filter: taker = 0xdb2e…c398; TIBBIR bought or sold
Result: rejected
Reason: estimated scan exceeded configured row and byte budgets
Status: UNAVAILABLE / REJECTED
```

### S030 — Bounded DEX aggregate preflight

```text
Operation: onchain-sql-preflight
Table: agent.base_dex_trades
Window: 2025-01-12 through 2025-01-19
Filter: taker = 0xdb2e…c398; TIBBIR bought or sold
Result: accepted
Status: YES
```

### S031 — Bounded DEX aggregate execution

```sql
SELECT min(block_time) AS first_trade,
       max(block_time) AS last_trade,
       countDistinct(tx_hash) AS tx_count,
       sum(amount_usd) AS one_sided_volume_usd,
       sum(token_bought_amount) AS bought_amount,
       sum(token_sold_amount) AS sold_amount
FROM agent.base_dex_trades
WHERE block_date >= toDate('2025-01-12')
  AND block_date < toDate('2025-01-20')
  AND block_time >= toDateTime('2025-01-12 00:00:00')
  AND block_time < toDateTime('2025-01-20 00:00:00')
  AND taker = '0xdb2eae229527135787c8cca1efa9e14888ffc398'
  AND (
    token_bought_address = '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00'
    OR token_sold_address = '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00'
  )
```

Result:

- first trade: 2025-01-12 00:35:17 UTC;
- last trade: 2025-01-19 22:04:05 UTC;
- distinct transactions: 74;
- summed one-sided notional: $216,098.96.

Status: YES for bounded launch-period aggregate.

### S032 — Conditional DEX aggregate preflight

```text
Operation: onchain-sql-preflight
Table: agent.base_dex_trades
Window: 2025-01-12 through 2025-01-19
Filter: taker = 0xdb2e…c398; TIBBIR bought or sold
Fields: distinct buy/sell rows, conditional amounts, TIBBIR amounts
Result: accepted
Status: YES
```

### S033 — Conditional DEX aggregate execution

```sql
SELECT countDistinct(tx_hash) AS tx_count,
       countIf(token_bought_address = '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00') AS buy_rows,
       countIf(token_sold_address = '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00') AS sell_rows,
       sumIf(amount_usd, token_bought_address = '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00') AS buy_one_sided_usd,
       sumIf(amount_usd, token_sold_address = '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00') AS sell_one_sided_usd,
       sumIf(token_bought_amount, token_bought_address = '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00') AS tibbir_bought_amount,
       sumIf(token_sold_amount, token_sold_address = '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00') AS tibbir_sold_amount
FROM agent.base_dex_trades
WHERE block_date >= toDate('2025-01-12')
  AND block_date < toDate('2025-01-20')
  AND block_time >= toDateTime('2025-01-12 00:00:00')
  AND block_time < toDateTime('2025-01-20 00:00:00')
  AND taker = '0xdb2eae229527135787c8cca1efa9e14888ffc398'
  AND (
    token_bought_address = '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00'
    OR token_sold_address = '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00'
  )
```

Result:

- buy rows: 51;
- sell rows: 29;
- TIBBIR bought: 81.10M;
- TIBBIR sold: 79.91M;
- buy-side one-sided value: $103,623.20;
- sell-side one-sided value: $112,475.76.

Status: YES for bounded TIBBIR trade aggregate.

### S034 — Later DEX trade transaction detail

```text
Operation: onchain-tx
Parameters: --chain base --hash 0x5f653e2601653c9a83cf8d798ae9eeeed1aa0680183ef243f7edbea21f36e9fe --include labels --json
Result:
- from = 0xdb2e…c398
- target = 0x6b2c…4d58
- target label = DEX Router (OKX)
Status: YES
```

---

## I. External Claim Context — Not On-Chain Evidence

These searches were used only to inventory public claims and contradictory token information. They did not affect address resolution, gates, scoring, or ownership conclusions.

### S035 — General claim searches

```text
search-web --q "TIBBIR Base creator wallet" --limit 10 --include-content
search-web --q "TIBBIR Micky Malka onchain" --limit 10 --include-content
search-web --q "TIBBIR token creator address Base" --limit 10 --include-content
search-web --q "0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00 creator wallet" --limit 10 --include-content
search-web --q "TIBBIR dev wallet address 0x" --limit 10 --include-content
```

### S036 — Candidate-address searches

```text
search-web --q "0xdb2eae229527135787c8cca1efa9e14888ffc398 TIBBIR" --limit 10 --include-content
search-web --q "0xdb2eae229527135787c8cca1efa9e14888ffc398 Micky Malka" --limit 10 --include-content
search-web --q "0x4213c040d6c82a64951f8d0b3721073eb1f9313e TIBBIR" --limit 10 --include-content
search-web --q "0x4213c040d6c82a64951f8d0b3721073eb1f9313e Micky Malka" --limit 10 --include-content
```

Status: Context only. External claims are not permitted to prove wallet ownership.

---

## J. Not Completed in This Run

The following were not completed and must remain unavailable in the per-wallet reports:

- complete first-ever funder analysis;
- top ten counterparties by USD and count;
- shared-funder SQL search;
- complete top-ten asset ranking;
- complete 7-day and 30-day current accumulation;
- contract-deployer verification;
- multisig/proxy ownership analysis;
- complete FIFO PnL;
- Smart Money Score calibration;
- ODEI board-state lookup.

---

## K. Ledger Sign-Off

```text
Ledger reproducibility: Pilot-ready
Provenance evidence: Confirmed for launch sender and allocation recipient
Person-wallet attribution: Not testable
Wallet analytics completeness: Partial
Smart Money Score: Insufficient
Production watchlist use: Not approved without additional fields and explicit scope
```

**Reviewer:** ____________________  
**Date:** ____________________  
**Ledger accepted:** Yes / With changes / No
