import unittest

from app import run


class AppTests(unittest.TestCase):
    def test_revised_api_envelope(self):
        payload = {"data": {"event": {"id": "evt-9", "status": "queued"}}}
        self.assertEqual(run(payload), {"id": "evt-9", "status": "queued"})


if __name__ == "__main__":
    unittest.main()
