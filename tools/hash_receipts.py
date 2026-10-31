#!/usr/bin/env python3
"""Hash wallet-pilot receipt CSVs for the receipt index (round fa7f9a3e).

Usage (on krypto, from the folder holding the receipt CSVs):
    python3 hash_receipts.py              # every *.csv in this folder
    python3 hash_receipts.py path/to/dir  # every *.csv in that folder
    python3 hash_receipts.py a.csv b.csv  # just these files

For each CSV it prints: S-ID (from the file name, or "pending" if none),
file, row count, SHA-256 of the file bytes, the grain/key type detected,
the key definition used, the number of unique keys, rows that collide on
the key, rows with a blank key part, and the canonical key hash.

Canonical key hash = SHA-256 of the key list: one key per row, fields joined
by ":", trimmed, lowercase, unique, sorted ascending, joined by LF, no
trailing newline (UTF-8).

Key per receipt type (detected from the columns, checked in this order):
  swap ledger, event grain   : tx_hash:evt_index             (S075, S079)
  swap ledger, tx grain      : tx_hash                       (S069)
  per-transfer pull          : tx_hash:direction:counterparty:token_address
                               (token_address if present, else asset/symbol)
                                                             (S076, S080, inventory)
  counterparty aggregate     : direction:counterparty:asset  (S073, S074)
  daily closes               : date:token_address            (S070-S078 closes)
  balance snapshot           : token_address                 (opening balances)

Why token_address before symbol for transfers: the 0xbe38 inventory has blank
symbols and homoglyph symbols (fake "USDC", "ETH"), so symbols collide.

A key hash alone does not prove equal rows when keys collide (e.g. two
identical transfers in one tx), so always publish the row count beside it.

Nothing is uploaded; the output is plain text to paste back into the chat.
"""
import csv
import glob
import hashlib
import json
import os
import re
import sys


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def pick(cols, *names):
    for n in names:
        if norm(n) in cols:
            return cols[norm(n)]
    return None


def key_spec(header):
    """Return (kind, [key columns]) for a receipt layout, or (None, None)."""
    cols = {norm(c): c for c in header}
    tx = pick(cols, "tx_hash", "transaction_hash", "hash")
    evt = pick(cols, "evt_index", "log_index", "event_index")
    direction = pick(cols, "direction")
    cp = pick(cols, "counterparty")
    tok = pick(cols, "token_address", "asset_address", "contract_address")
    asset = pick(cols, "asset", "token_symbol", "symbol")
    date = pick(cols, "date", "day", "block_date")
    sold = pick(cols, "token_sold_address", "token_sold_symbol")
    bought = pick(cols, "token_bought_address", "token_bought_symbol")

    if tx and evt:
        return "swap ledger, event grain", [tx, evt]
    if tx and direction and cp and (tok or asset):
        return "per-transfer", [tx, direction, cp, tok or asset]
    if tx and (sold or bought) and not direction:
        return "swap ledger, tx grain", [tx]
    if direction and cp and (asset or tok) and not tx:
        return "counterparty aggregate", [direction, cp, asset or tok]
    if date and tok:
        return "daily closes", [date, tok]
    if tok and not tx and not date:
        return "balance snapshot", [tok]
    return None, None


def hash_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = list(reader)
    kind, fields = key_spec(header)
    out = {
        "file": os.path.basename(path),
        "rows": len(rows),
        "csv_sha256": file_sha256(path),
        "key_type": kind or "UNRECOGNISED",
        "key_fields": ":".join(fields) if fields else None,
        "unique_keys": None,
        "colliding_rows": None,
        "rows_with_blank_key_part": None,
        "exact_duplicate_rows": len(rows) - len({tuple(r.get(c) for c in header) for r in rows}),
        "key_hash": None,
        "columns": header,
    }
    if fields:
        keys, blank = [], 0
        for r in rows:
            parts = [(r.get(c) or "").strip() for c in fields]
            if any(p == "" for p in parts):
                blank += 1
            keys.append(":".join(parts).lower())
        uniq = sorted(set(keys))
        out["unique_keys"] = len(uniq)
        out["colliding_rows"] = len(keys) - len(uniq)
        out["rows_with_blank_key_part"] = blank
        out["key_hash"] = hashlib.sha256("\n".join(uniq).encode("utf-8")).hexdigest()
    return out


def collect(args):
    if not args:
        args = ["."]
    files = []
    for a in args:
        if os.path.isdir(a):
            files += glob.glob(os.path.join(a, "*.csv"))
        else:
            files.append(a)
    return sorted(set(files))


def main():
    files = collect(sys.argv[1:])
    if not files:
        print("No .csv files found.")
        sys.exit(1)
    results = []
    for p in files:
        m = re.match(r"(S\d{3}(?:-S\d{3})?)", os.path.basename(p))
        r = hash_csv(p)
        r["s_id"] = m.group(1) if m else "pending"
        results.append(r)

    cols = ("s_id", "file", "rows", "csv_sha256", "key_type", "key_fields",
            "unique_keys", "colliding_rows", "rows_with_blank_key_part",
            "exact_duplicate_rows", "key_hash")
    print(" | ".join(cols))
    for r in results:
        print(" | ".join(str(r[k]) for k in cols))

    warn = [r for r in results if r["key_hash"] and (r["colliding_rows"] or r["rows_with_blank_key_part"])]
    if warn:
        print("\nKey warnings. The key hash counts each distinct key once, so a re-pull "
              "matches only if BOTH the key hash and the row count match:")
        for r in warn:
            print(f"  {r['file']}: {r['colliding_rows']} rows share a key with another row "
                  f"({r['exact_duplicate_rows']} of them are byte-identical rows), "
                  f"{r['rows_with_blank_key_part']} with a blank key part")
    unrec = [r for r in results if r["key_hash"] is None]
    if unrec:
        print("\nUnrecognised layouts (paste these column lists too):")
        for r in unrec:
            print(f"  {r['file']}: {r['columns']}")
    print("\nJSON:")
    print(json.dumps([{k: v for k, v in r.items() if k != "columns"} for r in results],
                     indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
