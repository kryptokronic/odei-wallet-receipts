# Multiset row hashes for receipts S069–S080 (first computed 2026-11-02, recomputed 2026-11-07)

Supplement to INDEX.csv for the next receipt index revision (Archon's 2026-11-02 request for duplicate-aware hashing). The key hash in INDEX.csv counts each distinct key once; the multiset row hash below keeps every row, so two files match on it only if they hold the same rows the same number of times.

Pinned to receipts at commit 8e56a134059540be5256c3702eb99e05145f5bf8. All values below were recomputed from those files on 2026-11-07 and equal the 2026-11-02 computation.

## Definition (serialization v1)

Every data row; all columns in header order; each value trimmed and lowercased; values joined by U+001F; rows sorted ascending with duplicates kept; rows joined by LF; no trailing newline; SHA-256 over UTF-8. Raw-byte file hashes (csv_sha256 in INDEX.csv) are separate and unchanged.

## Values

| Receipt | File | Rows | Multiset row hash |
|---|---|---:|---|
| S069 | receipts/S069_D_0xbe38_swap_ledger_tx_grain.csv | 289 | 8588b6f1008901f8d0edb80532ec58fec2e7b61d72896c9ba45538fc6a2b023f |
| S070–S072 (17 tokens) | receipts/S070-S072_shared_daily_closes_17tok.csv | 3060 | 919852624f112f6e0fc8e7a58bbedda72c301923ce1b72cfc5b2b458b84cc7b5 |
| S070–S072 (B20, 9 tokens) | receipts/S070-S072_shared_daily_closes_b20_9tok.csv | 792 | aa900f14befdee38ead97d71ba482579070f7f2a679d5cbc1572093190bd47bb |
| S073 | receipts/S073_D_0xbe38_counterparties_run1.csv | 29 | 21ab7904aa554da410bf46e4f5dba999779b0434cfe75eb423932f39082be262 |
| S074 | receipts/S074_D_0xbe38_counterparties_run2.csv | 125 | 500dc85b0cc29601bfec0a53763c3f285f4b8bc8fcb639cab7cd50845c10c9a6 |
| S075 | receipts/S075_A_0x0fd2_swap_ledger_event_grain.csv | 427 | 5a787ab2109f7bc287c3e1cd368e4533b9ca836642a39989f85cee446e02ac3d |
| S076 | receipts/S076_A_0x0fd2_transfers.csv | 396 | 687bcadae70cd53301e2606996c861e557427b0bfbe3bbcc41f655f400aeb237 |
| S077 | receipts/S077_A_0x0fd2_daily_closes_PA1.csv | 1320 | 37f9875c6a0b5f7eeacb1514d8fd4a773d7fdee891492a35255356cc8ed35f62 |
| S078 | receipts/S078_A_0x0fd2_daily_closes_PA2.csv | 1320 | 7320226fb3b5a886857032261afae738ced90f831cd946815a4c38efd8bad0af |
| S079 | receipts/S079_C_0xf043_swap_ledger_event_grain.csv | 331 | 97bf4ba2f7e88e7b804ccde3a5481735adf8f17bc2e75d1e67abf70c3ac97de5 |
| S080 | receipts/S080_C_0xf043_transfers.csv | 647 | 6941d305678a7af1776ad9028db25f5c6e3ca16bc2a8135e91492f8c463bcb8b |

## 0xbe38 inventory (data/D_0xbe38/base_wallet_transfers_0xbe38f8ae_20260501_20261028.csv)

- 5,204 rows, 5,141 unique keys (tx_hash:direction:counterparty:token_address); 50 keys carry 113 rows; 29 rows are exact duplicates, so 34 rows share a key but differ in values. No log index in the file. These collisions stay UNRESOLVED, not de-duplicated.
- Key hash (unique keys): bd1f46650685b55007874d46ec68873bdab6a1ce554034eba4b5bb5086d6839d (as INDEX.csv)
- Key-multiset hash (keys, duplicates kept, same serialization rules): b5bbbb6e4bbe8741474d5e843b244d1980cdeee5e15a02baea7ddc80fe857b07
- Multiset row hash: f4c299c40dd5d7b979950bb3e50de2a18961cb0df252ed3aaf2aecd6d06efb48

## S075 without its 12 blank-evt_index rows (Source Analyst request, reply 93a9810e)

415 rows / 415 unique keys (tx_hash:evt_index); key hash 38e9bbe53f7cf8f6d0c58552c0d3ec38bd1a15c121d33900c70bb578183d39a0. The 12 blank rows are in 12 distinct transactions.

These definitions are not final and will evolve with the data; feedback is welcome so they can be tuned fairly and equally.
