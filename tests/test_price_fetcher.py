import unittest
from src.products.price_fetcher import fetch_price

class TestPriceFetcher(unittest.TestCase):
    def test_invalid_url(self):
        with self.assertRaises(Exception):
            fetch_price("http://invalid.url", headers={"User-Agent": "test"})

if __name__ == "__main__":
    unittest.main()
