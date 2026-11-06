"""
Trade Journal CLI
-----------------
A tiny command-line journal for my trades.

Usage:
  python trade_journal.py add --symbol AAPL --side buy --qty 10 --price 225.50
  python trade_journal.py list
  python trade_journal.py summary

Trades are stored in trades.csv. The summary uses the average-cost
method: when you sell, profit = (sell price - average buy price) x qty.

Built by Kaushik Shivam while learning Python.
Standard library only (argparse, csv, os).
"""

import argparse
import csv
import os
from datetime import date

TRADES_FILE = "trades.csv"
FIELDS = ["date", "symbol", "side", "qty", "price"]


def load_trades():
    """Return all trades as a list of dicts (empty list if no file yet)."""
    if not os.path.exists(TRADES_FILE):
        return []
    with open(TRADES_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def add_trade(symbol, side, qty, price):
    """Append one trade to the CSV file (creating it if needed)."""
    new_file = not os.path.exists(TRADES_FILE)
    with open(TRADES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow({
            "date": date.today().isoformat(),
            "symbol": symbol.upper(),
            "side": side.lower(),
            "qty": qty,
            "price": price,
        })
    print(f"Added: {side.upper()} {qty} x {symbol.upper()} @ {price}")


def list_trades():
    trades = load_trades()
    if not trades:
        print("No trades recorded yet.")
        return
    print(f"{'Date':<12}{'Symbol':<10}{'Side':<6}{'Qty':>10}{'Price':>12}")
    print("-" * 50)
    for t in trades:
        print(f"{t['date']:<12}{t['symbol']:<10}{t['side']:<6}"
              f"{float(t['qty']):>10,.2f}{float(t['price']):>12,.2f}")


def summarise():
    """Work through trades in order, tracking position and realised P&L."""
    trades = load_trades()
    # stats[symbol] = {"qty": open qty, "avg_cost": ..., "realised": ...}
    stats = {}
    for t in trades:
        symbol = t["symbol"]
        qty = float(t["qty"])
        price = float(t["price"])
        s = stats.setdefault(symbol, {"qty": 0.0, "avg_cost": 0.0, "realised": 0.0})
        if t["side"] == "buy":
            # New average cost after adding this buy to the position
            total_cost = s["avg_cost"] * s["qty"] + price * qty
            s["qty"] += qty
            s["avg_cost"] = total_cost / s["qty"] if s["qty"] else 0.0
        else:  # sell
            s["realised"] += (price - s["avg_cost"]) * qty
            s["qty"] -= qty

    print(f"{'Symbol':<10}{'Open qty':>12}{'Avg cost':>12}{'Realised P&L':>15}")
    print("-" * 49)
    total = 0.0
    for symbol, s in stats.items():
        total += s["realised"]
        print(f"{symbol:<10}{s['qty']:>12,.2f}{s['avg_cost']:>12,.2f}"
              f"{s['realised']:>15,.2f}")
    print("-" * 49)
    print(f"{'TOTAL':<10}{'':>12}{'':>12}{total:>15,.2f}")


def main():
    parser = argparse.ArgumentParser(description="Simple trade journal")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a trade")
    p_add.add_argument("--symbol", required=True)
    p_add.add_argument("--side", required=True, choices=["buy", "sell"])
    p_add.add_argument("--qty", required=True, type=float)
    p_add.add_argument("--price", required=True, type=float)

    sub.add_parser("list", help="List all trades")
    sub.add_parser("summary", help="Show P&L per symbol")

    args = parser.parse_args()
    if args.command == "add":
        add_trade(args.symbol, args.side, args.qty, args.price)
    elif args.command == "list":
        list_trades()
    elif args.command == "summary":
        summarise()


if __name__ == "__main__":
    main()
