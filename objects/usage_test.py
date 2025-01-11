import unittest
from usage import Usage

class TestUsage(unittest.TestCase):
    def setUp(self):
        self.sample_usage_data = {
            "cap_reset_day": 10,
            "project_cap": "5000000000",
            "project_id": "1369785403853424",
            "project_usage": "43435"
        }

    def test_usage_from_dict(self):
        usage = Usage.from_dict(self.sample_usage_data)
        
        # Test basic attributes
        self.assertEqual(usage.cap_reset_day, 10)
        self.assertEqual(usage.project_cap, "5000000000")
        self.assertEqual(usage.project_id, "1369785403853424")
        self.assertEqual(usage.project_usage, "43435")

    def test_usage_with_empty_data(self):
        # Test with empty dict
        usage = Usage.from_dict({})
        
        self.assertEqual(usage.cap_reset_day, 0)
        self.assertEqual(usage.project_cap, "0")
        self.assertEqual(usage.project_id, "")
        self.assertEqual(usage.project_usage, "0")

        # Test with None
        usage = Usage.from_dict(None)
        
        self.assertEqual(usage.cap_reset_day, 0)
        self.assertEqual(usage.project_cap, "0")
        self.assertEqual(usage.project_id, "")
        self.assertEqual(usage.project_usage, "0")

if __name__ == '__main__':
    unittest.main() 