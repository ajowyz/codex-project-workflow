import unittest

from src.report import render_report


class ExistingBehaviorTests(unittest.TestCase):
    def test_zero_rows_are_hidden_by_default(self):
        records = [
            {"name": "alpha", "value": 3},
            {"name": "beta", "value": 0},
        ]
        self.assertEqual(render_report(records), "alpha: 3")


if __name__ == "__main__":
    unittest.main()
