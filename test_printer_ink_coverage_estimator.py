import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import estimate

def row(printer, yield_pages, printed, per_day):
    return {"printer": printer, "cartridge_yield_pages": str(yield_pages),
            "pages_printed": str(printed), "pages_per_day": str(per_day)}

class TestInkCoverage(unittest.TestCase):
    def test_days_left(self):
        r = estimate([row("HP-1", 2000, 1000, 50)])
        self.assertEqual((r[0][3], r[0][5]), (1000, 20))
    def test_coverage_percent(self):
        self.assertEqual(estimate([row("HP-1", 2000, 1000, 50)])[0][4], 50.0)
    def test_ok_when_14_or_more_days(self):
        self.assertEqual(estimate([row("HP-1", 2000, 1000, 50)])[0][6], "OK")
    def test_low_under_14_days(self):
        self.assertEqual(estimate([row("HP-1", 2000, 1500, 50)])[0][6], "LOW")
    def test_replace_under_3_days(self):
        self.assertEqual(estimate([row("HP-1", 2000, 1900, 50)])[0][6], "REPLACE")
    def test_exhausted(self):
        r = estimate([row("HP-1", 2000, 2000, 50)])[0]
        self.assertEqual((r[3], r[6]), (0, "EXHAUSTED"))
    def test_over_yield_is_exhausted(self):
        self.assertEqual(estimate([row("HP-1", 2000, 2100, 50)])[0][6], "EXHAUSTED")
    def test_zero_pages_per_day_unknown(self):
        self.assertIsNone(estimate([row("HP-1", 2000, 1000, 0)])[0][5])
    def test_fewest_days_first(self):
        r = estimate([row("A", 2000, 1000, 50), row("B", 2000, 1900, 50)])
        self.assertEqual(r[0][0], "B")
