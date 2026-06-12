import unittest

from src.invoice import format_invoice_id


class InvoiceTests(unittest.TestCase):
    def test_invoice_id_is_six_digits(self):
        self.assertEqual("INV-000042", format_invoice_id(42))

    def test_invoice_id_keeps_six_digit_number(self):
        self.assertEqual("INV-654321", format_invoice_id(654321))


if __name__ == "__main__":
    unittest.main()
