#!/usr/bin/env python3
"""Merge the wallet-pilot download files into one searchable long-format CSV.

Every source row becomes one output row. Common fields are mapped into shared
columns (time, tx_hash, token, amount, counterparty...), and the full original
row is kept verbatim in raw_json, so nothing is lost.
"""
import csv, hashlib, json, os, re, sys

csv.field_size_limit(10**9)
IN, OUT = sys.argv[1], sys.argv[2]

WALLETS = {
    "0xbe38f8aebea16e0b3b268042771e6507f1f15d73": "D (pilot)",
    "0x0fd279161e2346eb514a98f31c01bb8a19c6b1d2": "A (pilot)",
    "0xf043d4f8748f189ec881cb6a72018748331c5544": "C (pilot)",
    "0xa311f7ca3eb2fb98123a807f9b8e4bbbdbdcb2ee": "E (sourcing r1)",
    "0x1c3a0684": "F (sourcing r1)",
    "0xb71aaf88d47195044fc52c99c7eb3638e44649f8": "G (sourcing r1)",
    "0x702733dde6f9637286a4282a7ec2784702184189": "H (round 2, Drop)",
    "0x8797a47a9200b52ee90b4c5b5fa5a0ded56dd5f5": "I (round 2, Monitor)",
    "0x3014cd18c535658e1ad10cc95bced1ddd9d12426": "I cluster funder",
    "0xfffc54d82ab10adec849ae344db7517f68d88be8": "hub 0xfffc54d8 (T4 operator contract)",
}

# file -> (dataset description, record_type, subject address or None, wallet label)
FILES = {
    "base_wallet_transfers_0xbe38f8ae_20260501_20261028.csv": ("D full inventory: every transfer (S-ID pending; byte-identical to project receipt)", "transfer", "0xbe38f8aebea16e0b3b268042771e6507f1f15d73"),
    "base_0xbe38f8aebea16e0b3b268042771e6507f1f15d73_token_balances_2026-05-01.csv": ("D opening balances 2026-05-01 (S-ID pending)", "balance", "0xbe38f8aebea16e0b3b268042771e6507f1f15d73"),
    "base_dex_swaps_0x1c3a0684_20260501_20261028_1.csv": ("F swap ledger, event grain", "swap_event", "0x1c3a0684"),
    "base-dex-swaps-2026-05-01-to-2026-10-28.csv": ("G swap ledger, event grain (identified: all 272 txs appear in G's transfer pull)", "swap_event", "0xb71aaf88d47195044fc52c99c7eb3638e44649f8"),
    "base_transfers_0xb71aaf88_2026-05-01_2026-10-28.csv": ("G every transfer", "transfer", "0xb71aaf88d47195044fc52c99c7eb3638e44649f8"),
    "base-wallet-inbound-erc20-2026-05-01-to-2026-10-28.csv": ("G inbound ERC-20 transfers (identified: tx_from is G on 768 of 1096 rows)", "transfer", "0xb71aaf88d47195044fc52c99c7eb3638e44649f8"),
    "base_0xb71aaf88_balances_20260501.csv": ("G opening balances 2026-05-01", "balance", "0xb71aaf88d47195044fc52c99c7eb3638e44649f8"),
    "base_0x7027_erc20_native_transfers_2026-05-01_2026-10-28.csv": ("H every ERC-20 + native transfer", "transfer", "0x702733dde6f9637286a4282a7ec2784702184189"),
    "z_bb9d532d-attachments_1/base_dex_swaps_0x702733dde6f9637286a4282a7ec2784702184189_2026-05-01_2026-10-28.csv": ("H swap ledger, event grain", "swap_event", "0x702733dde6f9637286a4282a7ec2784702184189"),
    "z_bb9d532d-attachments_1/base_swaps_token_amount_flags.csv": ("H swap token decimals/amount flags", "token_flag", "0x702733dde6f9637286a4282a7ec2784702184189"),
    "base_token_daily_close_volume_2026-05-01_2026-10-27.csv": ("H traded tokens: daily close + DEX volume (identified: all 13 tokens are in H's swaps)", "daily_close", "0x702733dde6f9637286a4282a7ec2784702184189"),
    "z_9b411742-attachments_2/transfers_0x7027_vs_deployers_and_pools.csv": ("H S6 serial-launch test: transfers vs deployers and pools", "transfer", "0x702733dde6f9637286a4282a7ec2784702184189"),
    "z_9b411742-attachments_2/base_token_launch_details.csv": ("H S6 test: launch details of H's tokens", "launch", "0x702733dde6f9637286a4282a7ec2784702184189"),
    "z_9b411742-attachments_2/deployer_counterparty_check.csv": ("H S6 test: deployer counterparty check", "summary", "0x702733dde6f9637286a4282a7ec2784702184189"),
    "z_9b411742-attachments_2/base_first5_buyers_first_hour.csv": ("H S6 test: first 5 buyers in first hour per token", "launch", "0x702733dde6f9637286a4282a7ec2784702184189"),
    "base_transfers_0xfffc54d8_2026-04-01_2026-10-28.csv": ("Hub 0xfffc54d8 transfers (no token_address column in source)", "transfer", "0xfffc54d82ab10adec849ae344db7517f68d88be8"),
    "base-address-due-diligence.csv": ("Hub / infrastructure address due diligence (7 addresses)", "address_profile", None),
    "base_addresses_eth_weth_flows_and_sell_settlement_2026-04-01_2026-10-28.csv": ("Round-2 candidates: ETH/WETH inflows and sell settlement path", "address_profile", None),
    "base_wallets_matched_pnl.csv": ("Round-2 sourcing screen: matched P&L per wallet", "address_profile", None),
    "z_ad568fbf-attachments_3/base_dex_swaps_0x8797a47a_20260501_20261028.csv": ("I swap ledger, event grain", "swap_event", "0x8797a47a9200b52ee90b4c5b5fa5a0ded56dd5f5"),
    "z_ad568fbf-attachments_3/base_dex_swaps_unknown_token_manifest.csv": ("I swaps: unknown-token (raw amount) manifest", "token_flag", "0x8797a47a9200b52ee90b4c5b5fa5a0ded56dd5f5"),
    "z_ee829760-attachments_4/transfers.csv": ("I transfers (tx_from is I on 154 of 327 rows)", "transfer", "0x8797a47a9200b52ee90b4c5b5fa5a0ded56dd5f5"),
    "z_ee829760-attachments_4/launches.csv": ("I traded tokens: launch provenance (incl. LOTTO)", "launch", "0x8797a47a9200b52ee90b4c5b5fa5a0ded56dd5f5"),
    "z_1c9f9184-attachments_5/swaps_3014.csv": ("I Test 3: swap ledger of funder 0x3014", "swap_event", "0x3014cd18c535658e1ad10cc95bced1ddd9d12426"),
    "z_1c9f9184-attachments_5/links.csv": ("I Test 3: transfers linking 0x3014 / 0x32a5 / I", "transfer", "0x3014cd18c535658e1ad10cc95bced1ddd9d12426"),
    "z_1c9f9184-attachments_5/profiles.csv": ("I Test 3: address profiles (0x3014, 0x32a5)", "address_profile", None),
}
SKIP = {
    "base_0x7027_erc20_native_transfers_2026-05-01_2026-10-28_Copy.csv": "byte-identical duplicate of the H transfers file; not merged twice",
}

B2 = "/tmp/claude-0/-home-claude/eefcfb82-e31e-51b3-ab96-595a41ba7cef/scratchpad/in2/"
FILES.update({
    B2+"base_0xbe38f8aebea16e0b3b268042771e6507f1f15d73_dex_swaps_20260501_20261028.csv": ("D swap ledger, tx grain (receipt)", "swap_event", "0xbe38f8aebea16e0b3b268042771e6507f1f15d73", "S069"),
    B2+"base-token-daily-close-dex-volume-2026-05-01-to-2026-10-27.csv": ("Shared daily closes, 17 tokens (receipt)", "daily_close", "", "S070-S072"),
    B2+"base-b20-daily-2026-08-01-to-2026-10-27.csv": ("Shared daily closes, 9 B20 tokens (receipt)", "daily_close", "", "S070-S072"),
    B2+"base-wallet-counterparties-2026-05-01-to-2026-10-28.csv": ("D counterparty aggregate, run 1 (receipt)", "summary", "0xbe38f8aebea16e0b3b268042771e6507f1f15d73", "S073"),
    B2+"base-wallet-counterparties-2026-05-01-to-2026-10-28_1.csv": ("D counterparty aggregate, run 2 (receipt)", "summary", "0xbe38f8aebea16e0b3b268042771e6507f1f15d73", "S074"),
    B2+"base-dex-swaps-0fd27916-20260501-20261028.csv": ("A swap ledger, event grain (receipt; 12 blank evt_index)", "swap_event", "0x0fd279161e2346eb514a98f31c01bb8a19c6b1d2", "S075"),
    B2+"base-wallet-0x0fd279-transfers-2026-05-01-to-2026-10-28.csv": ("A per-transfer pull (receipt)", "transfer", "0x0fd279161e2346eb514a98f31c01bb8a19c6b1d2", "S076"),
    B2+"base_tokens_daily_close_volume_20260801_20261027.csv": ("A traded tokens daily closes, set 1 (receipt)", "daily_close", "0x0fd279161e2346eb514a98f31c01bb8a19c6b1d2", "S077"),
    B2+"base_tokens_daily_close_volume_20260801_20261027_1.csv": ("A traded tokens daily closes, set 2 (receipt)", "daily_close", "0x0fd279161e2346eb514a98f31c01bb8a19c6b1d2", "S078"),
    B2+"base_dex_swaps_f043d4f8_20260501_20261028.csv": ("C swap ledger, event grain (receipt)", "swap_event", "0xf043d4f8748f189ec881cb6a72018748331c5544", "S079"),
    B2+"base_wallet_0xf043_txflow_2026-05-01_2026-10-28.csv": ("C per-transfer pull (receipt)", "transfer", "0xf043d4f8748f189ec881cb6a72018748331c5544", "S080"),
    B2+"base_dex_swaps_0xa311f7ca_20260501-20261028.csv": ("E swap ledger, event grain", "swap_event", "0xa311f7ca3eb2fb98123a807f9b8e4bbbdbdcb2ee"),
    B2+"base_wallets_2026-05-01_2026-10-28.csv": ("Sourcing round 1 screen: activity, funders, 7702 flag (15 wallets)", "address_profile", None),
    B2+"base_smart_money_15.csv": ("Sourcing round 1 screen: realised P&L and win rate (15 wallets)", "address_profile", None),
})
SKIP[B2+"base_dex_swaps_0x1c3a0684_20260501_20261028.csv"] = "byte-identical duplicate of the F swap file (_1); not merged twice"

COLS = ["record_id", "s_id", "source_file", "source_sha256", "source_row", "dataset", "record_type",
        "wallet_label", "subject_address", "block_time_utc", "block_number", "tx_hash", "evt_index",
        "direction", "token_address", "token_symbol", "amount", "amount_usd",
        "token_sold_address", "token_sold_symbol", "token_sold_amount",
        "token_bought_address", "token_bought_symbol", "token_bought_amount",
        "counterparty", "counterparty_label", "tx_from", "flag", "note", "raw_json"]

ALIASES = {
    "block_time_utc": ["block_time", "block_time_utc", "date", "first_buy_time_utc", "deploy_time_utc", "deploy_block_time"],
    "tx_hash": ["tx_hash", "first_buy_tx", "deploy_tx"],
    "direction": ["direction", "direction_from_0x7027"],
    "token_address": ["token_address", "contract_address"],
    "token_symbol": ["token_symbol", "symbol", "asset"],
    "amount": ["amount", "amount_decimals_adjusted", "balance"],
    "counterparty": ["counterparty", "counterparty_address", "from_address", "buyer_address", "from"],
    "amount_usd": ["amount_usd", "total_usd", "realised_pnl_usd", "matched_pnl_usd"],
    "counterparty_label": ["counterparty_label", "from_label", "counterparty_role", "surf_label"],
    "flag": ["flag", "label_type"],
    "note": ["note", "notes"],
}
DIRECT = ["block_number", "evt_index", "token_sold_address", "token_sold_symbol",
          "token_sold_amount", "token_bought_address", "token_bought_symbol", "token_bought_amount", "tx_from"]


def iso(t):
    t = (t or "").strip()
    if not t:
        return ""
    m = re.match(r"(\d{4}-\d{2}-\d{2})(?:[ T](\d{2}:\d{2}(?::\d{2})?))?", t)
    if not m:
        return t
    d, hms = m.group(1), m.group(2)
    if not hms:
        return d
    if len(hms) == 5:
        hms += ":00"
    return f"{d}T{hms}Z"


def label_for(addr):
    a = (addr or "").lower()
    for k, v in WALLETS.items():
        if a.startswith(k):
            return v
    return ""


def main():
    manifest = []
    n = 0
    with open(OUT, "w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(fo, fieldnames=COLS)
        w.writeheader()
        for rel, spec in FILES.items():
            desc, rtype, subj = spec[:3]
            sid = spec[3] if len(spec) > 3 else ""
            path = rel if os.path.isabs(rel) else os.path.join(IN, rel)
            sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
            base = os.path.basename(rel)
            with open(path, newline="", encoding="utf-8-sig") as fi:
                rd = csv.DictReader(fi)
                cnt = 0
                for i, r in enumerate(rd, start=2):
                    o = {c: "" for c in COLS}
                    for col, names in ALIASES.items():
                        for nm in names:
                            if r.get(nm) not in (None, ""):
                                o[col] = r[nm]
                                break
                    for col in DIRECT:
                        o[col] = r.get(col, "") or ""
                    o["block_time_utc"] = iso(o["block_time_utc"])
                    s = subj or r.get("address", "") or r.get("deployer_address", "")
                    o.update(record_id=f"{base}#{i}", s_id=sid, source_file=base, source_sha256=sha, source_row=i,
                             dataset=desc, record_type=rtype, subject_address=s.lower(),
                             wallet_label=label_for(s),
                             raw_json=json.dumps(r, ensure_ascii=False, separators=(",", ":")))
                    w.writerow(o)
                    cnt += 1
            n += cnt
            manifest.append((base, rel, sha, cnt, desc, "merged"))
        # the blocked research.start payload: one document row
        jp = [f for f in os.listdir(IN) if f.endswith(".json")]
        for f in jp:
            p = os.path.join(IN, f)
            raw = open(p, encoding="utf-8").read()
            sha = hashlib.sha256(raw.encode()).hexdigest()
            o = {c: "" for c in COLS}
            o.update(record_id=f"{f}#1", source_file=f, source_sha256=sha, source_row=1,
                     dataset="ODEI research.start payload blocked 2026-10-29 (retry must reuse it unchanged)",
                     record_type="document", note="see raw_json", raw_json=json.dumps(json.loads(raw), ensure_ascii=False))
            w.writerow(o)
            n += 1
            manifest.append((f, f, sha, 1, o["dataset"], "merged as one document row"))
    for f, why in SKIP.items():
        p = f if os.path.isabs(f) else os.path.join(IN, f)
        manifest.append((os.path.basename(f), f, hashlib.sha256(open(p, "rb").read()).hexdigest(), 0, why, "not merged (duplicate)"))
    with open(OUT.replace(".csv", "-manifest.csv"), "w", newline="", encoding="utf-8") as fm:
        mw = csv.writer(fm)
        mw.writerow(["file", "path_in_download_or_zip", "sha256", "rows_merged", "what_it_is", "status"])
        mw.writerows(manifest)
    print("rows", n, "files", len(manifest))


if __name__ == "__main__":
    main()
