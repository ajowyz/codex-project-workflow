import tempfile
import unittest
from pathlib import Path

from product.modeling import ModelProject
from product.storage import write_json


class ModelingTests(unittest.TestCase):
    def test_direct_module_and_storage(self):
        project = ModelProject()
        model = project.add_model("demo", "cube")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "model.json"
            write_json(target, model)
            self.assertTrue(target.is_file())


if __name__ == "__main__":
    unittest.main()
