# ODEI wallet-research pilot: receipts and data

Private data store for the Masters Chief multi-agent wallet-research pilot on ODEI Network (round `fa7f9a3e`, receipt verification idea `6dd76e5f`). On-chain behaviour on Base only; nothing here identifies any person. Framework text, scoring weights and role prompts are **not** stored here.

## Layout

| Folder | What it holds |
|---|---|
| `receipts/` | Gate receipts S069–S080, renamed by S-ID. Bytes are exactly as returned by the provider. |
| `data/<wallet>/` | Other pulls per wallet: D 0xbe38 full inventory, E 0xa311, F 0x1c3a, G 0xb71a, H 0x7027 (S6 serial-launch test), I 0x8797 (incl. Test 3 cluster), hub 0xfffc54d8, sourcing screens. S-IDs pending for these. |
| `tibbir-test/` | TIBBIR v1.2 gate-fail dry run: per-wallet reports, fixture results, source ledger (TIBBIR-S001–S036). |
| `merged/` | One searchable CSV of everything (41,463 rows, with `s_id`, `wallet_label` and the full source row in `raw_json`) plus its manifest, zipped. |
| `docs/` | Decisions and corrections, e.g. the S073/S074 prompt and scope record. |
| `tools/` | `hash_receipts.py` (row count, file SHA-256, canonical key hash), merge scripts. |
| `INDEX.csv` | Every CSV here: path, rows, file SHA-256, key type, key fields, distinct keys, collisions, blank key parts, key hash. |

## Verify a file

```
python3 tools/hash_receipts.py receipts/
```

Compare `csv_sha256` and `key_hash` with `INDEX.csv`. A re-pull matches only if **both** the key hash and the row count match (keys can collide, e.g. the D inventory has 63 rows sharing a key).

Key hash = SHA-256 of the canonical key list: one key per row, fields joined by `:`, trimmed, lowercase, unique, sorted, LF-joined, no trailing newline. Keys: event-grain swap ledger `tx_hash:evt_index`; tx-grain ledger (S069) `tx_hash`; per-transfer `tx_hash:direction:counterparty:asset` (token_address if present); counterparty aggregate (S073/S074) `direction:counterparty:asset`; daily closes `date:token_address`; balance snapshot `token_address`. Address-profile files have no row key; use the file SHA-256.

## Known notes (2026-10-31)

- All 11 receipt key hashes match the values recorded on 2026-10-29.
- S073/S074 are two runs of the same prompt (P4); the provider applied "exclude DEX pools/routers" differently. See `docs/`.
- S075 has 12 rows with a blank `evt_index`.
- G2 (scale gate) = one-sided DEX scale excluding quote-to-quote swaps; 0xf043 (C) fails it ($45,468.73) and is withdrawn as a GO wallet.

## Rules

- Never edit a file in place. A corrected pull is a new file with a new S-ID; update `INDEX.csv` in the same commit.
- `.gitattributes` disables line-ending conversion so the hashes stay valid.
