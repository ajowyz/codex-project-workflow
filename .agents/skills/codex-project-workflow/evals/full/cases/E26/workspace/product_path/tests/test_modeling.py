import unittest

from product.modeling import ModelProject


class ModelingTests(unittest.TestCase):
    def test_model_shape(self):
        project = ModelProject()
        self.assertEqual(
            project.add_model("demo", "cube"),
            {"name": "demo", "shape": "cube", "version": 1},
        )


if __name__ == "__main__":
    unittest.main()
