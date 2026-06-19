from src.main import substructure_search
import unittest


class TestSubstructureSearch(unittest.TestCase):
    def test_same_molecules(self):
        self.assertEqual(
            substructure_search(
                ["C1CC1", "C1CC1", "C1CC1"],
                "C1CC1"),
            ["C1CC1", "C1CC1", "C1CC1"]
            )

    def test_different_molecules(self):
        self.assertEqual(
            substructure_search(
                ["CCO", "c1ccccc1", "CC(=O)O", "CC(=O)Oc1ccccc1C(=O)O"],
                "c1ccccc1"),
            ["c1ccccc1", "CC(=O)Oc1ccccc1C(=O)O"]
            )


if __name__ == '__main__':
    unittest.main()
