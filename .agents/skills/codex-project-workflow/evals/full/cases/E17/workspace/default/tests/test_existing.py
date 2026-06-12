import unittest

from reading_list import ReadingList


class ExistingTests(unittest.TestCase):
    def test_items_preserve_insertion_order(self):
        reading_list = ReadingList()
        reading_list.add("https://example.test/one")
        reading_list.add("https://example.test/two")
        self.assertEqual(
            reading_list.items(),
            ["https://example.test/one", "https://example.test/two"],
        )


if __name__ == "__main__":
    unittest.main()
