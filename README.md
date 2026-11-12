# printer-ink-coverage-estimator

Estimate how many days of printing a cartridge has left from a CSV: pages left = yield minus printed, days left = pages left / pages per day — EXHAUSTED at 0 pages, REPLACE under 3 days, LOW under 14 days, otherwise OK, fewest days first.

## How to run

```sh
python3 main.py printers.csv
```

## Example output

```
HP-Office: REPLACE (100 page(s) left, 95.0% used, 2 day(s) remaining)
HP-Lab: OK (1000 page(s) left, 50.0% used, 20 day(s) remaining)
1 printer(s) need a cartridge now.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
