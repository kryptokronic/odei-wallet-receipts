#!/usr/bin/env python3
"""Append the TIBBIR v1.2 test package (markdown) to the merged wallet-pilot CSV.

One row per section (split on headings). Source-ledger entries "### S0NN — ..."
get s_id TIBBIR-S0NN (prefixed so they never collide with the pilot ledger's
S001-S101) and their Operation / Status / Use lines mapped into columns.
The section's full markdown text is kept verbatim in raw_json.
"""
import csv, hashlib, json, os, re, sys

csv.field_size_limit(10**9)
MERGED, MDDIR = sys.argv[1], sys.argv[2]
TIBBIR = "0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00"
DOCS = {
    "odei-source-ledger-tibbir-v1.2.md": "TIBBIR v1.2 test: source ledger (one row per call)",
    "odei-per-wallet-reports-tibbir-v1.2.md": "TIBBIR v1.2 test: per-wallet reports (0xdb2e, 0x4213)",
    "odei-fixture-results-tibbir-v1.2.md": "TIBBIR v1.2 test: fixture results A-D",
}

with open(MERGED, newline="", encoding="utf-8") as f:
    cols = next(csv.reader(f))

out = []
for name, desc in DOCS.items():
    path = os.path.join(MDDIR, name)
    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    lines = raw.decode("utf-8").splitlines()
    sections, cur, stack, start = [], [], [], 1
    for i, ln in enumerate(lines, 1):
        m = re.match(r"^(#{1,4})\s+(.*)", ln)
        if m:
            if cur and any(x.strip() for x in cur):
                sections.append((start, " > ".join(stack), "\n".join(cur)))
            lvl = len(m.group(1))
            stack = stack[:lvl - 1] + [m.group(2).strip()]
            cur, start = [ln], i
        else:
            cur.append(ln)
    if cur and any(x.strip() for x in cur):
        sections.append((start, " > ".join(stack), "\n".join(cur)))
    wallet = ""
    for start, heading, text in sections:
        o = {c: "" for c in cols}
        w = re.search(r"Wallet \d+ — `(0x[0-9a-f]{4}…[0-9a-f]{4})`", heading)
        if w:
            wallet = w.group(1)
        sid = re.search(r"\b(S\d{3})\b —", heading.split(" > ")[-1])
        def field(k):
            m = re.search(rf"^{k}:\s*(.*)$", text, re.M)
            return m.group(1).strip() if m else ""
        o.update(record_id=f"{name}#L{start}", s_id=f"TIBBIR-{sid.group(1)}" if sid else "",
                 source_file=name, source_sha256=sha, source_row=start, dataset=desc,
                 record_type="ledger_call" if sid else "document_section",
                 wallet_label="TIBBIR test" + (f" wallet {wallet}" if wallet and "wallet-reports" in name else ""),
                 subject_address=wallet if "wallet-reports" in name else "",
                 token_address=TIBBIR, token_symbol="TIBBIR",
                 flag=field("Status"), note=(heading + (" | " + field("Use") if field("Use") else ""))[:500],
                 tx_hash=(re.search(r"\b0x[0-9a-f]{64}\b", text) or [""])[0],
                 raw_json=json.dumps({"heading": heading, "operation": field("Operation"),
                                      "parameters": field("Parameters"), "text": text}, ensure_ascii=False))
        out.append(o)

with open(MERGED, "a", newline="", encoding="utf-8") as f:
    csv.DictWriter(f, fieldnames=cols).writerows(out)
print("appended", len(out))
