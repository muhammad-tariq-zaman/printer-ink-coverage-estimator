"""Estimate how many days of printing a cartridge has left.

Usage: python3 main.py printers.csv
CSV columns: printer,cartridge_yield_pages,pages_printed,pages_per_day.
Pages left = cartridge yield - pages printed.
Days left = pages left / pages per day.
- EXHAUSTED: no pages left.
- REPLACE: fewer than 3 days left.
- LOW: fewer than 14 days left.
- OK: 14 days or more left.
Coverage used = pages printed / yield * 100. Fewest days left first.
"""
import argparse, csv, sys

def estimate(rows):
    out = []
    for row in rows:
        yield_pages = int(row["cartridge_yield_pages"])
        printed = int(row["pages_printed"])
        per_day = int(row["pages_per_day"])
        remaining = yield_pages - printed
        coverage = round(printed / yield_pages * 100, 1) if yield_pages else 0.0
        if remaining <= 0:
            days_left = 0
            verdict = "EXHAUSTED"
        elif per_day <= 0:
            days_left = None
            verdict = "OK"
        else:
            days_left = remaining // per_day
            if days_left < 3:
                verdict = "REPLACE"
            elif days_left < 14:
                verdict = "LOW"
            else:
                verdict = "OK"
        out.append((row["printer"].strip(), yield_pages, printed, remaining,
                    coverage, days_left, verdict))
    return sorted(out, key=lambda r: (r[5] if r[5] is not None else 10 ** 9, r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = estimate(list(csv.DictReader(f)))
    for printer, yield_pages, printed, remaining, coverage, days_left, verdict in results:
        days = "unknown" if days_left is None else f"{days_left} day(s)"
        print(f"{printer}: {verdict} ({remaining} page(s) left, {coverage:.1f}% used, {days} remaining)")
    print(f"{sum(1 for *_, v in results if v in ('EXHAUSTED', 'REPLACE'))} printer(s) need a cartridge now.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
