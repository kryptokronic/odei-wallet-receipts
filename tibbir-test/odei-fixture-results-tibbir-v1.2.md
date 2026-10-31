# ODEI v1.2 Fixture Results — TIBBIR Base Test

**Run date:** 2026-10-28 UTC  
**Fixture family:** TIBBIR launch provenance and wallet-analysis test  
**Primary ledger:** `odei-source-ledger-tibbir-v1.2.md`  
**Framework under test:** ODEI Wallet Research Framework v1.2

---

## 1. Test Summary

The TIBBIR investigation exercised the most important v1.2 controls using two on-chain-derived addresses:

- `0xdb2e…c398`: launch transaction sender.
- `0x4213…313e`: initial allocation recipient.

The test confirmed that the framework can reconstruct direct launch relationships and preserve identity uncertainty. It also exposed several failures in the previous execution that are now addressed in v1.2.

### Overall result

```text
Provenance controls: PASS with terminology corrections
Data-reconciliation controls: PASS
Identity-boundary controls: PASS
Score-discipline controls: PASS
Strict-chain-scope controls: FAIL in original run; corrected in v1.2
Lookback controls: FAIL in original run; corrected in v1.2
Volume-semantics controls: FAIL in original run; corrected in v1.2
Production readiness: NOT YET APPROVED
```

---

## 2. Fixture Results

| Fixture | Test objective | Original result | v1.2 result | Evidence |
|---|---|---|---|---|
| A | Explicit Base wallet and strict scope | FAIL | Open validation | Aggregate EVM values were presented alongside Base values |
| B | Inferred launch sender | FAIL in wording | PASS after role correction | Launch sender is no longer called creator by default |
| C | Initial allocation recipient | FAIL in wording | PASS after role correction | Allocation recipient is no longer called dev wallet by default |
| D | Empty wallet endpoint versus valid SQL | PASS with caveat | PASS | SQL activity overrides empty endpoint for supported fields only |
| E | Bounded first-event query | PASS | PASS | Broad query rejected; bounded query accepted; partition rule preserved |
| F | Public-person attribution claim | PASS | PASS | Result is `IDENTITY_NOT_TESTABLE` without permitted attestation |
| G | Incomplete trading history | PASS | PASS | Score returned `NA / INSUFFICIENT` |
| H | One-sided DEX volume semantics | FAIL in wording | PASS after metric correction | `$216.1K` is observed one-sided notional, not gross volume |
| I | Parent protocol versus token project | PARTIAL | PASS after validation rule | Project detail must match target symbol and contract |
| J | Failed and rejected call logging | FAIL | PASS after source-ledger requirement | Rejected preflights and failed lookups must be recorded |

---

## 3. Fixture A — Strict Base Scope

### Objective

Run a Base wallet investigation without contaminating Base-specific fields with aggregate EVM values.

### Observed behavior

The wallet-detail endpoint returned:

- Base chain balance of approximately $2.05;
- aggregate EVM value of approximately $10.07;
- multiple active EVM chains.

The previous report displayed both but did not make the scope distinction sufficiently prominent.

### Result

```text
Original: FAIL
v1.2: OPEN VALIDATION
```

### Required control

For `STRICT_CHAIN_SCOPE=yes`:

- Base fields use Base data only.
- Aggregate EVM data is secondary context.
- No chain-specific net-worth or DeFi conclusion is made from an endpoint without a chain filter.

### Acceptance criterion

A reviewer must be able to identify which value is Base-only and which is aggregate EVM without reading the source ledger.

---

## 4. Fixture B — Inferred Launch Sender

### Objective

Resolve an address from a launch transaction without overcalling it a creator wallet.

### Observed evidence

`0xdb2e…c398` was the sender of the initial TIBBIR launch transaction targeting the labeled Virtuals bonding proxy.

### Result

```text
Original: FAIL in role vocabulary
v1.2: PASS after correction
```

### Correct role

```text
launch_transaction_sender
```

### Prohibited role without additional evidence

```text
creator_wallet
contract_deployer
Micky Malka wallet
```

### Acceptance criterion

The report must state that transaction initiation is confirmed while contract deployment and human ownership remain unestablished.

---

## 5. Fixture C — Initial Allocation Recipient

### Objective

Identify the recipient of the initial mint without labeling it a development or team wallet.

### Observed evidence

`0x4213…313e` received 875,870,016 TIBBIR in the initial mint transaction.

### Result

```text
Original: FAIL in role vocabulary
v1.2: PASS after correction
```

### Correct role

```text
initial_allocation_recipient
```

### Prohibited role without explicit evidence

```text
dev_wallet
team_wallet
treasury
Micky Malka wallet
```

### Acceptance criterion

The report must not infer a team role from a large initial allocation alone.

---

## 6. Fixture D — Empty Endpoint versus Valid SQL

### Objective

Ensure an empty wallet-transfer response is not mistaken for no activity when direct SQL returns valid rows.

### Observed behavior

`wallet-transfers` returned empty data for the candidate wallets. On-chain SQL and wallet-history returned launch-related activity.

### Result

```text
PASS with reconciliation note
```

### Required handling

- Endpoint state: `UNAVAILABLE` or `PARTIAL` for the affected transfer field.
- SQL state: valid for the exact fields returned.
- No claim that the wallet had no transfers.
- Conflict recorded in completeness and source ledger.

### Acceptance criterion

The report must distinguish “endpoint returned no data” from “wallet had no activity.”

---

## 7. Fixture E — Bounded First-Event Query

### Objective

Prevent a bounded partition query from being reported as an absolute first event.

### Observed behavior

The unbounded historical transfer query was rejected because it attempted to scan more than the accepted partition range. A bounded query covering 2024-10-28 through 2025-10-27 was accepted and returned the initial mint events.

### Result

```text
PASS
```

### Acceptance criterion

- Rejected broad preflight is logged.
- Accepted bounded query is logged.
- Minimum timestamp is checked against the partition floor.
- Result is called “first observed within validated coverage” unless all-time coverage is proven.

---

## 8. Fixture F — Public-Person Attribution

### Objective

Test a claim that an on-chain wallet belongs to a named public person.

### Observed claim

Community content claimed that a wallet associated with TIBBIR was connected to Micky Malka.

### Result

```text
PASS
```

### Required result

```text
IDENTITY_NOT_TESTABLE
```

unless a Surf entity label or user-supplied cryptographic attestation is provided.

### Acceptance criterion

The report may confirm wallet-to-token or wallet-to-protocol transactions but must not confirm wallet-to-person ownership.

---

## 9. Fixture G — Incomplete Trading History

### Objective

Prevent an incomplete wallet history from producing a misleading Smart Money Score.

### Observed behavior

Launch-period TIBBIR activity was measurable, but complete top-ten token history, BTC-relative returns, FIFO PnL, and multi-token maturity were not established.

### Result

```text
PASS
```

### Required result

```text
smart_money_score = NA
band = INSUFFICIENT
```

### Acceptance criterion

The report must not convert missing returns into losses or assign `No edge` when the score is not computable.

---

## 10. Fixture H — DEX Volume Semantics

### Objective

Prevent one-sided DEX values from being mislabeled as gross volume.

### Observed behavior

The DEX table returned approximately $216.1K of summed `amount_usd` across TIBBIR launch-period trades. The table defines `amount_usd` as one-sided token-sold value.

### Result

```text
Original: FAIL in terminology
v1.2: PASS after correction
```

### Correct field

```text
observed_dex_notional_usd = SUM(amount_usd)
```

Optional:

```text
two_sided_proxy_volume_usd = 2 × observed_dex_notional_usd
```

Neither is realized PnL.

---

## 11. Fixture I — Parent Protocol versus Target Token

### Objective

Prevent fuzzy project lookup from assigning parent-protocol team or ownership data to the target token.

### Observed behavior

`project-detail --q TIBBIR` returned Virtuals Protocol context and included the TIBBIR contract.

### Result

```text
PASS after validation rule
```

### Required control

Use project-level data only when:

- returned token symbol matches the target;
- returned contract and chain match the target;
- the field is relevant to the target rather than only the parent protocol.

---

## 12. Fixture J — Failed and Rejected Call Logging

### Objective

Ensure the source ledger contains unsuccessful attempts.

### Observed failures

- Fuzzy project detail for `Ribbita` returned an upstream error after retries.
- Broad transfer SQL preflight was rejected for excessive partition span.
- Broad DEX SQL preflight was rejected for scan-budget excess.

### Result

```text
Original: FAIL
v1.2: PASS after source-ledger requirement
```

### Acceptance criterion

A peer reviewer must be able to see what was attempted, what failed, why it failed, and which narrower call replaced it.

---

## 13. Remaining Fixture Work

The following fixtures were not fully executed in the TIBBIR run and remain open:

- complete first-funder analysis;
- top-ten counterparties by USD and count;
- shared-funder SQL analysis;
- full top-ten token history;
- full 7-day and 30-day accumulation analysis;
- contract-deployer verification;
- multisig or proxy ownership detection;
- score calibration against a known wallet dataset.

These must not be marked as passing merely because the TIBBIR provenance sub-run succeeded.

---

## 14. Peer-Review Decision

```text
Provenance fixture coverage:      Pilot pass
Identity boundary:                Pass
Failure handling:                 Pass with source-ledger correction
Strict chain scope:               Open
Trading-score calibration:        Open
Production release:               Not approved
```

**Reviewer:** ____________________  
**Date:** ____________________  
**Decision:** Approve / Approve with changes / Reject
