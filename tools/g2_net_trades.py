#!/usr/bin/env python3
"""G2 economic-scale counter, rule 2 (net per-transaction trades, A15), Wallet Research v1.2.2.

Usage:
    python3 -I tools/g2_net_trades.py receipts/S079_C_0xf043_swap_ledger_event_grain.csv [out.csv]

Rule (frozen 2026-11-01, policy id G2-R2 v1):
  1. Group the wallet's swap rows by (chain, tx_hash). Chain is Base for every pilot receipt.
  2. Net delta per token address in the tx:  net[t] = SUM(token_bought_amount where bought = t)
                                                     - SUM(token_sold_amount   where sold   = t)
     Intermediate hops (A->B->C) cancel; tokens recycled inside the tx (sold, then partly bought
     back) are netted. Tokens are identified by contract address, never by symbol.
  3. Drop tokens whose net is exactly 0 (exact decimal arithmetic on the CSV strings).
  4. If no remaining token is a non-quote token, the tx is ALL_QUOTE and is not a trade (A19).
  5. Otherwise the tx is ONE net trade. Class: BUY (non-quote only in), SELL (non-quote only out),
     SWAP (non-quote on both sides), MIXED (non-quote in and out plus quote out, i.e. a sell
     and a buy settled in one tx).
  6. Implied USD price of token t in this tx:
        p[t] = SUM(amount_usd of the tx's rows with amount_usd > 0 in which t is either leg)
             / SUM(t's amount on those rows)
     amount_usd comes from the provider (Surf) as recorded in the receipt. No outside prices.
  7. Trade value = SUM over tokens with net[t] < 0 of  -net[t] * p[t]   ("net sold side").
     If any net-sold token has no price, the trade is UNPRICED: listed, but not added to G2.
  8. G2 scale = SUM of priced trade values. Pass at 50,000 USD (8.2). The 5% margin rule
     (G2-MARGIN TEST v0.1) is reported separately and never changes the original result.

Refunds: a router refund arrives as a transfer, not a swap event, so it is invisible to rule 2
when only the swap ledger exists. With a full A24 transfer pull the same netting is applied to
all of the wallet's token transfers in the tx; without one the gap is flagged.
"""
import collections
import csv
import sys
from decimal import Decimal

QUOTE = {  # A19 quote list by contract address (Base)
    "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913": "USDC",
    "0xfde4c96c8593536e31f229ea8f37b2ada2699bb2": "USDT",
    "0x60a3e35cc302bfa44cb288bc5a4f316fdb1adb42": "EURC",
    "0x526728dbc96689597f85ae4cd716d4f7fccbae9d": "msUSD",
    "0xe5020a6d073a794b6e7f05678707de47986fb0b6": "frxUSD",
    "0x4200000000000000000000000000000000000006": "WETH",
    "0x0000000000000000000000000000000000000000": "ETH",
    "0x2ae3f1ec7f1f5012cfeab0185bfc7aa3cf0dec22": "cbETH",
    "0xc1cba3fcea344f92d9239c08c0568f6f2f0ee452": "wstETH",
    "0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf": "cbBTC",
    "0xecac9c5f704e954931349da37f60e39f515c11c1": "LBTC",
    "0x236aa50979d5f3de3bd1eeb40e81137f22ab794b": "tBTC",
}


def dec(x):
    return Decimal(x) if x not in (None, "") else None


def run(path):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8-sig")))
    txs = collections.OrderedDict()
    for r in rows:
        txs.setdefault(r["tx_hash"].lower(), []).append(r)
    trades = []
    for h, ev in txs.items():
        net = collections.defaultdict(Decimal)
        usd = collections.defaultdict(Decimal)
        amt = collections.defaultdict(Decimal)
        sym = {}
        for e in ev:
            s, b = e["token_sold_address"].lower(), e["token_bought_address"].lower()
            sa, ba, u = dec(e["token_sold_amount"]), dec(e["token_bought_amount"]), dec(e["amount_usd"])
            sym[s], sym[b] = e["token_sold_symbol"] or s[:10], e["token_bought_symbol"] or b[:10]
            net[s] -= sa
            net[b] += ba
            if u is not None and u > 0:
                usd[s] += u; amt[s] += sa
                usd[b] += u; amt[b] += ba
        nz = {t: v for t, v in net.items() if v != 0}
        nq_in = [t for t, v in nz.items() if t not in QUOTE and v > 0]
        nq_out = [t for t, v in nz.items() if t not in QUOTE and v < 0]
        if not nq_in and not nq_out:
            cls = "ALL_QUOTE"
        elif nq_in and not nq_out:
            cls = "BUY"
        elif nq_out and not nq_in:
            cls = "SELL"
        elif any(t in QUOTE and v < 0 for t, v in nz.items()):
            cls = "MIXED"
        else:
            cls = "SWAP"
        value, unpriced = Decimal(0), []
        if cls != "ALL_QUOTE":
            for t, v in nz.items():
                if v < 0:
                    if amt[t] == 0:
                        unpriced.append(sym[t])
                    else:
                        value += -v * usd[t] / amt[t]
        trades.append({
            "chain": "base", "tx_hash": h, "block_time": ev[0]["block_time"], "events": len(ev),
            "class": cls,
            "net_deltas": "; ".join(f"{sym[t]}({t}) {v:+}" for t, v in nz.items()),
            "status": "EXCLUDED_ALL_QUOTE" if cls == "ALL_QUOTE" else ("UNPRICED:" + "|".join(unpriced) if unpriced else "COUNTED"),
            "value_usd": "" if cls == "ALL_QUOTE" or unpriced else f"{value:.6f}",
        })
    return trades


def main():
    trades = run(sys.argv[1])
    counted = [t for t in trades if t["status"] == "COUNTED"]
    total = sum(Decimal(t["value_usd"]) for t in counted)
    unp = [t for t in trades if t["status"].startswith("UNPRICED")]
    allq = [t for t in trades if t["class"] == "ALL_QUOTE"]
    print(f"tx {len(trades)} | net trades {len(counted) + len(unp)} (priced {len(counted)}, unpriced {len(unp)}) | all-quote excluded {len(allq)}")
    print(f"G2 rule 2 = {total:.2f} USD | vs 50,000: {(total / 50000 - 1) * 100:+.2f}%")
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(trades[0]))
            w.writeheader()
            w.writerows(trades)


if __name__ == "__main__":
    main()
