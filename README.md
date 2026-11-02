# ODEI wallet-research pilot: receipts and data

Open data store for the Masters Chief multi-agent wallet-research pilot on ODEI Network (round `fa7f9a3e`, receipt verification idea `6dd76e5f`). On-chain behaviour on Base only; nothing here identifies any person. Framework text, scoring weights and role prompts are **not** stored here. Published openly on 2026-11-02 so any participant can re-pull and check the receipts. None of the pilot's decisions are final: they will change with what the data shows, and feedback is weighed on its evidence, equally, whoever it comes from.

## Layout

| Folder | What it holds |
|---|---|
| `receipts/` | Gate receipts S069–S080, renamed by S-ID. Bytes are exactly as returned by the provider. |
| `data/<wallet>/` | Other pulls per wallet: D 0xbe38 full inventory, E 0xa311, F 0x1c3a, G 0xb71a, H 0x7027 (S6 serial-launch test), I 0x8797 (incl. Test 3 cluster), hub 0xfffc54d8, sourcing screens. S-IDs pending for these. |
| `tibbir-test/` | TIBBIR v1.2 gate-fail dry run: per-wallet reports, fixture results, source ledger (TIBBIR-S001–S036). |
| `merged/` | One searchable CSV of everything (41,463 rows, with `s_id`, `wallet_label` and the full source row in `raw_json`) plus its manifest, zipped. |
| `docs/` | Decisions and corrections: the S073/S074 prompt and scope record; the G2 rule 2 spec with worked examples and margin sensitivity. |
| `derived/` | Computed outputs, e.g. G2 rule 2, one row per transaction for each pilot wallet. |
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
- G2 (scale gate), updated 2026-11-01: rule 2, net per-transaction trades (`docs/2026-11-01-g2-net-trade-spec.md`, `tools/g2_net_trades.py`). 0xf043 (C) = $48,595.30, 2.81% below $50,000: original result FAIL, included under the versioned policy exception G2-MARGIN TEST v0.1, tagged BOUNDARY, Monitor-only. The earlier $45,468.73 figure is withdrawn.

## Rules

- Never edit a file in place. A corrected pull is a new file with a new S-ID; update `INDEX.csv` in the same commit.
- `.gitattributes` disables line-ending conversion so the hashes stay valid.
