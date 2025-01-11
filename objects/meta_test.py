import unittest
from meta import Meta

class TestMeta(unittest.TestCase):
    def setUp(self):
        self.sample_meta_data = {
            "oldest_id": "1258085245091368960",
            "newest_id": "1337498609819021312",
            "result_count": 100,
            "next_token": "7140w"
        }

        self.sample_meta_data_with_prev = {
            "result_count": 3,
            "next_token": "18LAA581J5II7LA00C00ZZZZ",
            "previous_token": "1BLC45G1H8CAL5DG0G00ZZZZ"
        }

    def test_meta_from_dict(self):
        meta = Meta.from_dict(self.sample_meta_data)
        
        # Test basic attributes
        self.assertEqual(meta.result_count, 100)
        self.assertEqual(meta.oldest_id, "1258085245091368960")
        self.assertEqual(meta.newest_id, "1337498609819021312")
        self.assertEqual(meta.next_token, "7140w")
        self.assertIsNone(meta.previous_token)

    def test_meta_with_previous_token(self):
        meta = Meta.from_dict(self.sample_meta_data_with_prev)
        
        # Test with previous token
        self.assertEqual(meta.result_count, 3)
        self.assertEqual(meta.next_token, "18LAA581J5II7LA00C00ZZZZ")
        self.assertEqual(meta.previous_token, "1BLC45G1H8CAL5DG0G00ZZZZ")
        self.assertIsNone(meta.oldest_id)
        self.assertIsNone(meta.newest_id)

    def test_meta_with_empty_data(self):
        # Test with empty dict
        meta = Meta.from_dict({})
        
        self.assertIsNone(meta.result_count)
        self.assertIsNone(meta.oldest_id)
        self.assertIsNone(meta.newest_id)
        self.assertIsNone(meta.next_token)
        self.assertIsNone(meta.previous_token)

        # Test with None
        meta = Meta.from_dict(None)
        
        self.assertIsNone(meta.result_count)
        self.assertIsNone(meta.oldest_id)
        self.assertIsNone(meta.newest_id)
        self.assertIsNone(meta.next_token)
        self.assertIsNone(meta.previous_token)

if __name__ == '__main__':
    unittest.main() 