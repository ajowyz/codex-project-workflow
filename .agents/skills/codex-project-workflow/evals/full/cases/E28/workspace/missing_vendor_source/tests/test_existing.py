import tempfile
import unittest
from pathlib import Path

from service import process_event
from state_store import JsonStateStore


class ExistingTests(unittest.TestCase):
    def test_single_event_is_processed(self):
        with tempfile.TemporaryDirectory() as directory:
            result = process_event(
                {"id": "evt-1", "type": "payment.paid"},
                JsonStateStore(Path(directory) / "state.json"),
            )
        self.assertEqual(result, {"accepted": True, "duplicate": False})


if __name__ == "__main__":
    unittest.main()
