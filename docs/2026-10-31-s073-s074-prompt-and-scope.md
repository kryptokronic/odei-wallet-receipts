# S073 / S074: prompt and scope difference (recorded 2026-10-31)

**Wallet:** D, 0xbe38f8aebea16e0b3b268042771e6507f1f15d73 (Base). **Window:** 2026-05-01 to 2026-10-28.
**Source:** "Wallet research" chat, 2026-10-28 (P4, turns 104–107). Public correction posted on idea 6dd76e5f as reply 8d2c4e71 to 3b8e6f2a.

## Prompt P4 (both runs, verbatim)

```
For Base wallet 0xbe38f8aebea16e0b3b268042771e6507f1f15d73, 2026-05-01 to 2026-10-28: list every counterparty that sent it ETH, WETH, USDC, USDT, DAI or cbBTC worth ≥ $100, and every counterparty it sent those assets to (exclude DEX pools/routers). CSV: direction, counterparty, asset, total_usd, tx_count, first_ts, last_ts, surf_label, label_type (CEX/fund/bridge/mixer/sanctioned/exploit/unknown). Flag any counterparty that both sent to and received from the wallet. No estimates.
```

## Runs

| S-ID | File | Rows | Key hash (direction:counterparty:asset) | How Surf applied "exclude DEX pools/routers" |
|---|---|---:|---|---|
| S073 | base-wallet-counterparties-2026-05-01-to-2026-10-28.csv | 29 | fee264dc848c29ad07c512efa9d286c7542dd1e2bdf6534a7aabd8ac509eb7b5 | Excluded any counterparty whose label contained pool, router, adapter, AMM or a DEX classification. Directions in/out; labels populated. 1,922 transfer rows returned, 1,018 valued. |
| S074 | base-wallet-counterparties-2026-05-01-to-2026-10-28_1.csv | 125 | dfec2171588e42164712952d8a4570cabf5f8ab00a94fc35dc82c7f90080f44c | Excluded only four identified DEX addresses: 0x67d03631…81df DexRouter, 0x6cdcb1c4…971d Aerodrome Volatile AMM, 0x8f10b468…f996 Kyber, 0x52308454…10b7 Aerodrome CLPool. Directions received/sent; nearly all labels "unknown". Threshold applied to aggregated total_usd. |

## Findings (computed 2026-10-31 from the original files)

- All 29 S073 rows appear in S074 with identical direction, counterparty, asset, total_usd and tx_count.
- S074 adds 96 rows ($506.5K); 61 of them flow in both directions, consistent with unlabelled pools (inference).
- The A17 swap-hash exclusion does not explain the gap: 43 of the 96 extra rows have no swap-hash link to S069, and 17 transfers inside S073's rows do share one.

## Decision as posted

- S073 is the run that matches the prompt's intent; S074 is kept as evidence that the exclusion is not reproducible. Neither is a reproducible receipt (the exclusion depends on provider labels, which change between runs).
- Re-pull test for P4: subset test. Supports if all 29 S073 keys are present with totals within 1%; extra rows are reported, not counted as a mismatch.
- S3/S4 screens for D stay PARTIAL.
- Correction to the data state of two receipts under check 9091ec33: NOT CARRIED until the receipt index is published.

## Lesson for future counterparty pulls

Do not rely on the provider to exclude DEX pools/routers. Pull per-transfer rows with counterparty_has_code and labels, then exclude pools locally by contract address and the A17 swap-hash rule, so the exclusion is reproducible.
