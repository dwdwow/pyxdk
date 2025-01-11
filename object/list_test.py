import unittest
from datetime import datetime
from list import List
from user import User

class TestList(unittest.TestCase):
    def setUp(self):
        self.sample_list_data = {
            "name": "Twitter Comms",
            "member_count": 60,
            "id": "1355797419175383040",
            "private": False,
            "description": "",
            "follower_count": 198,
            "owner_id": "257366942",
            "created_at": "2021-01-31T08:37:48.000Z"
        }

        self.sample_api_response = {
            "data": self.sample_list_data,
            "includes": {
                "users": [{
                    "created_at": "2011-02-25T07:51:26.000Z",
                    "name": "Ashleigh Hay 🤸🏼‍♀️",
                    "id": "257366942",
                    "username": "shleighhay",
                    "verified": False,
                    "description": "",
                    "protected": False,
                    "entities": {}
                }]
            }
        }

    def test_list_from_dict(self):
        twitter_list = List.from_dict(self.sample_list_data)
        
        # Test basic attributes
        self.assertEqual(twitter_list.id, "1355797419175383040")
        self.assertEqual(twitter_list.name, "Twitter Comms")
        self.assertEqual(twitter_list.member_count, 60)
        self.assertEqual(twitter_list.follower_count, 198)
        self.assertEqual(twitter_list.owner_id, "257366942")
        self.assertFalse(twitter_list.private)
        self.assertEqual(twitter_list.description, "")
        
        # Test datetime conversion
        self.assertIsInstance(twitter_list.created_at, datetime)
        self.assertEqual(twitter_list.created_at.year, 2021)
        self.assertEqual(twitter_list.created_at.month, 1)
        self.assertEqual(twitter_list.created_at.day, 31)
        self.assertEqual(twitter_list.created_at.hour, 8)
        self.assertEqual(twitter_list.created_at.minute, 37)
        self.assertEqual(twitter_list.created_at.second, 48)

    def test_list_from_api_response(self):
        result = List.from_api_response(self.sample_api_response)
        
        # Test structure
        self.assertIn('data', result)
        self.assertIn('includes', result)
        self.assertIn('users', result['includes'])
        
        # Test list
        twitter_list = result['data']
        self.assertIsInstance(twitter_list, List)
        self.assertEqual(twitter_list.id, "1355797419175383040")
        self.assertEqual(twitter_list.name, "Twitter Comms")
        
        # Test included users
        self.assertEqual(len(result['includes']['users']), 1)
        user = result['includes']['users'][0]
        self.assertIsInstance(user, User)
        self.assertEqual(user.id, "257366942")
        self.assertEqual(user.name, "Ashleigh Hay 🤸🏼‍♀️")
        self.assertEqual(user.username, "shleighhay")

    def test_list_with_missing_optional_fields(self):
        # Test data without optional description
        data_without_description = self.sample_list_data.copy()
        del data_without_description['description']
        
        twitter_list = List.from_dict(data_without_description)
        self.assertIsNone(twitter_list.description)
        
        # Other required fields should still be present
        self.assertEqual(twitter_list.id, "1355797419175383040")
        self.assertEqual(twitter_list.name, "Twitter Comms")

if __name__ == '__main__':
    unittest.main() 