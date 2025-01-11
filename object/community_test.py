import unittest
from datetime import datetime
from community import Community

class TestCommunity(unittest.TestCase):
    def setUp(self):
        self.sample_community_data = {
            "id": "Q29tbXVuaXR5OjE3NTg3NDc4MTc2NDI3MDA5MjI=",
            "description": "Welcome to the Anime Community! Where anime fans gather to share their favorite shows and discuss everything anime-related.",
            "join_policy": "Open",
            "access": "Public",
            "member_count": 39915,
            "name": "Anime Community",
            "created_at": "2024-02-17T06:58:50.000Z"
        }

        self.sample_api_response = {
            "data": [
                self.sample_community_data,
                {
                    "id": "Q29tbXVuaXR5OjE1MDY3OTM5NTMxMDYwNDI4OTE=",
                    "description": "Join and text about anime 🥰",
                    "join_policy": "Open",
                    "access": "Public",
                    "member_count": 26019,
                    "name": "Anime World 🌸",
                    "created_at": "2022-03-24T00:44:07.000Z"
                }
            ],
            "meta": {
                "next_token": "7140dibdnow9c7btw481s8m561gat797rboud5r80xvzm"
            }
        }

    def test_community_from_dict(self):
        community = Community.from_dict(self.sample_community_data)
        
        # Test basic attributes
        self.assertEqual(community.id, "Q29tbXVuaXR5OjE3NTg3NDc4MTc2NDI3MDA5MjI=")
        self.assertEqual(community.name, "Anime Community")
        self.assertEqual(community.join_policy, "Open")
        self.assertEqual(community.access, "Public")
        self.assertEqual(community.member_count, 39915)
        self.assertEqual(
            community.description,
            "Welcome to the Anime Community! Where anime fans gather to share their favorite shows and discuss everything anime-related."
        )
        
        # Test datetime conversion
        self.assertIsInstance(community.created_at, datetime)
        self.assertEqual(community.created_at.year, 2024)
        self.assertEqual(community.created_at.month, 2)
        self.assertEqual(community.created_at.day, 17)
        self.assertEqual(community.created_at.hour, 6)
        self.assertEqual(community.created_at.minute, 58)
        self.assertEqual(community.created_at.second, 50)

    def test_community_from_api_response(self):
        result = Community.from_api_response(self.sample_api_response)
        
        # Test structure
        self.assertIn('data', result)
        self.assertIn('meta', result)
        
        # Test communities
        self.assertEqual(len(result['data']), 2)
        community = result['data'][0]
        self.assertIsInstance(community, Community)
        self.assertEqual(community.id, "Q29tbXVuaXR5OjE3NTg3NDc4MTc2NDI3MDA5MjI=")
        self.assertEqual(community.name, "Anime Community")
        
        # Test second community
        community2 = result['data'][1]
        self.assertEqual(community2.name, "Anime World 🌸")
        self.assertEqual(community2.member_count, 26019)
        
        # Test meta data
        self.assertEqual(
            result['meta']['next_token'],
            "7140dibdnow9c7btw481s8m561gat797rboud5r80xvzm"
        )

if __name__ == '__main__':
    unittest.main() 