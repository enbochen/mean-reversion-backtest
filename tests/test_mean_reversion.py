import unittest
from src.mean_reversion import MeanReversionStrategy
from src.data_loader import load_data
import pandas as pd
import numpy as np


class TestMeanReversionStrategy(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            'timestamp': pd.to_datetime([
                '2020-01-01 00:00:00', '2020-01-01 01:00:00',
                '2020-01-01 02:00:00', '2020-01-01 03:00:00',
                '2020-01-01 04:00:00'
            ]),
            'close': [100, 101, 100, 102, 103],
        }

        self.df = pd.DataFrame(self.test_data)
        self.strategy = MeanReversionStrategy(self.df, mean_period_in_hour=4)

    def test_calculate_mean(self):
        self.strategy.calculate_mean()
        expected_mean = [100.0, 100.5, 100.33333333333333, 100.75, 101.2]
        actual_mean = self.strategy.data['mean'].tolist()
        # Check if the calculated mean is close to the expected mean
        self.assertTrue(np.allclose(actual_mean, expected_mean,
                        rtol=1e-05, atol=1e-08, equal_nan=True))

    def test_load_data(self):
        data = load_data('data/ohlc.csv')
        self.assertIsInstance(data, pd.DataFrame)
        self.assertTrue('open' in data.columns)
        self.assertTrue('close' in data.columns)
        self.assertTrue('high' in data.columns)
        self.assertTrue('low' in data.columns)
        self.assertTrue('vol' in data.columns)

# more test methods can be added here for other functions and methods


if __name__ == '__main__':
    unittest.main()
