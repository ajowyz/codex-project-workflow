import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "workspace" / "writable_docs"


class DocumentConsistencyTests(unittest.TestCase):
    def test_documents_keep_catalog_ownership(self):
        architecture = (ROOT / "docs" / "ARCHITECTURE.md").read_text(
            encoding="utf-8"
        )
        integration = (ROOT / "docs" / "INTEGRATION.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("catalog service owns", architecture.lower())
        self.assertNotIn("checkout owns publication status", integration.lower())
        self.assertNotIn("catalog imports checkout", integration.lower())

    def test_plan_records_no_implementation_contract(self):
        plan = (ROOT / "docs" / "PLAN.md").read_text(encoding="utf-8")
        self.assertIn("implementation contract: none", plan.lower())


if __name__ == "__main__":
    unittest.main()
