import unittest
from datetime import datetime
from space import Space
from user import User

class TestSpace(unittest.TestCase):
    def setUp(self):
        self.sample_space_data = {
            "id": "1zqKVXPQhvZJB",
            "state": "live",
            "created_at": "2021-07-04T23:12:08.000Z",
            "host_ids": [
                "2244994945",
                "6253282"
            ],
            "lang": "en",
            "is_ticketed": False,
            "invited_user_ids": [
                "2244994945",
                "6253282"
            ],
            "participant_count": 420,
            "scheduled_start": "2021-07-14T08:00:00.000Z",
            "speaker_ids": [
                "2244994945",
                "6253282"
            ],
            "started_at": "2021-07-14T08:00:12.000Z",
            "title": "Say hello to the Space data object!",
            "updated_at": "2021-07-11T14:44:44.000Z"
        }

        self.sample_api_response = {
            "data": self.sample_space_data,
            "includes": {
                "users": [
                    {
                        "id": "2244994945",
                        "name": "Twitter Dev",
                        "username": "TwitterDev"
                    },
                    {
                        "id": "6253282",
                        "name": "Twitter API",
                        "username": "TwitterAPI"
                    }
                ]
            }
        }

    def test_space_from_dict(self):
        space = Space.from_dict(self.sample_space_data)
        
        # Test basic attributes
        self.assertEqual(space.id, "1zqKVXPQhvZJB")
        self.assertEqual(space.state, "live")
        self.assertEqual(space.lang, "en")
        self.assertFalse(space.is_ticketed)
        self.assertEqual(space.title, "Say hello to the Space data object!")
        
        # Test datetime conversions
        self.assertIsInstance(space.created_at, datetime)
        self.assertEqual(space.created_at.year, 2021)
        self.assertEqual(space.created_at.month, 7)
        self.assertEqual(space.created_at.day, 4)
        
        # Test lists
        self.assertEqual(len(space.host_ids), 2)
        self.assertIn("2244994945", space.host_ids)
        self.assertIn("6253282", space.host_ids)
        
        # Test optional fields
        self.assertEqual(space.participant_count, 420)
        self.assertIsInstance(space.scheduled_start, datetime)
        self.assertIsInstance(space.started_at, datetime)

    def test_space_from_api_response(self):
        result = Space.from_api_response(self.sample_api_response)
        
        # Test structure
        self.assertIn('data', result)
        self.assertIn('includes', result)
        self.assertIn('users', result['includes'])
        
        # Test space
        space = result['data']
        self.assertIsInstance(space, Space)
        self.assertEqual(space.id, "1zqKVXPQhvZJB")
        
        # Test included users
        self.assertEqual(len(result['includes']['users']), 2)
        user = result['includes']['users'][0]
        self.assertIsInstance(user, User)
        self.assertEqual(user.id, "2244994945")
        self.assertEqual(user.name, "Twitter Dev")

if __name__ == '__main__':
    unittest.main() 