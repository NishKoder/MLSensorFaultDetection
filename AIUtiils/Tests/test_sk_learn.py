import unittest
import pandas as pd
from AIUtiils.scikit_learn import perform_train_test_split

class TestPerformTrainTestSplit(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.data = pd.DataFrame({
            'feature1': range(10),
            'feature2': range(10, 20),
            'target': range(20, 30)
        })

    def test_split_ratio(self):
        train_set, test_set = perform_train_test_split(self.data, test_size=0.2)
        self.assertEqual(len(train_set), 8)
        self.assertEqual(len(test_set), 2)

    def test_split_content(self):
        train_set, test_set = perform_train_test_split(self.data, test_size=0.2)
        self.assertTrue('feature1' in train_set.columns)
        self.assertTrue('feature2' in train_set.columns)
        self.assertTrue('target' in train_set.columns)
        self.assertTrue('feature1' in test_set.columns)
        self.assertTrue('feature2' in test_set.columns)
        self.assertTrue('target' in test_set.columns)

if __name__ == '__main__':
    unittest.main()