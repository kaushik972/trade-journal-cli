# Trade Journal CLI

A simple command-line journal for recording trades and seeing your profit/loss per symbol.

## Why I built this

I've traded stocks and forex on my own for about 7 years, and the biggest lesson is that you can't improve what you don't record. I used to keep trades in messy notes; this little tool keeps them in one CSV file and tells me my realised P&L per symbol using the average-cost method — the same way I'd work it out by hand, but without the mistakes.

## What it does

- `add` — record a trade (symbol, buy/sell, quantity, price); it is appended to `trades.csv` with today's date
- `list` — show all recorded trades
- `summary` — per symbol: open quantity, average cost, and realised P&L, plus a total

## How to run

```bash
cd trade-journal-cli
python trade_journal.py add --symbol AAPL --side buy --qty 10 --price 225.50
python trade_journal.py list
python trade_journal.py summary
```

## Demo (using the included sample `trades.csv`)

`python trade_journal.py summary` gives:

```
Symbol        Open qty    Avg cost   Realised P&L
-------------------------------------------------
USDJPY            0.00      154.20         850.00
AAPL              0.00      226.37          80.75
EURUSD            0.00        1.08         -12.00
7203.T          100.00    2,650.00           0.00
-------------------------------------------------
TOTAL                                      918.75
```

Reading it: the USDJPY round trip made 850.00, AAPL made 80.75, EURUSD lost 12.00, and the Toyota (7203.T) position is still open — 100 shares at an average cost of 2,650.

## Files

- `trade_journal.py` — the program (uses `argparse`)
- `trades.csv` — sample trades to try the demo; your own trades get added to this file

## Next steps

- Support short positions properly in the summary
- Add fees/commissions per trade
- Weekly review report: win rate and best/worst trades

*Standard library only. Built while learning Python.*
