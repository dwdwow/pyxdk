import unittest
from datetime import datetime
from user import User, UserEntities, UrlEntity, HashtagEntity
from tweet import Tweet

class TestUser(unittest.TestCase):
    def setUp(self):
        self.sample_user_data = {
            "id": "2244994945",
            "name": "Twitter Dev",
            "username": "TwitterDev",
            "location": "127.0.0.1",
            "entities": {
                "url": {
                    "urls": [{
                        "start": 0,
                        "end": 23,
                        "url": "https://t.co/3ZX3TNiZCY",
                        "expanded_url": "/content/developer-twitter/en/community",
                        "display_url": "developer.twitter.com/en/community"
                    }]
                },
                "description": {
                    "hashtags": [{
                        "start": 23,
                        "end": 30,
                        "tag": "DevRel"
                    }, {
                        "start": 113,
                        "end": 130,
                        "tag": "BlackLivesMatter"
                    }]
                }
            },
            "verified": True,
            "description": "The voice of Twitter's #DevRel team...",
            "url": "https://t.co/3ZX3TNiZCY",
            "profile_image_url": "https://pbs.twimg.com/profile_images/1267175364003901441/tBZNFAgA_normal.jpg",
            "protected": False,
            "pinned_tweet_id": "1255542774432063488",
            "created_at": "2013-12-14T04:35:55.000Z"
        }

        self.sample_api_response = {
            "data": [self.sample_user_data],
            "includes": {
                "tweets": [{
                    "id": "1255542774432063488",
                    "text": "During these unprecedented times...",
                    "edit_history_tweet_ids": ["1255542774432063488"],
                    "author_id": "2244994945",
                    "created_at": "2020-04-29T17:01:38.000Z",
                    "lang": "en",
                    "possibly_sensitive": False,
                    "public_metrics": {
                        "retweet_count": 0,
                        "reply_count": 0,
                        "like_count": 0,
                        "quote_count": 0
                    }
                }]
            }
        }

    def test_user_from_dict(self):
        user = User.from_dict(self.sample_user_data)
        
        # Test basic attributes
        self.assertEqual(user.id, "2244994945")
        self.assertEqual(user.name, "Twitter Dev")
        self.assertEqual(user.username, "TwitterDev")
        self.assertEqual(user.location, "127.0.0.1")
        self.assertTrue(user.verified)
        self.assertFalse(user.protected)
        
        # Test datetime conversion
        self.assertIsInstance(user.created_at, datetime)
        self.assertEqual(user.created_at.year, 2013)
        self.assertEqual(user.created_at.month, 12)
        self.assertEqual(user.created_at.day, 14)
        
        # Test entities
        self.assertIsInstance(user.entities, UserEntities)
        self.assertIsInstance(user.entities.url['urls'][0], UrlEntity)
        self.assertIsInstance(user.entities.description['hashtags'][0], HashtagEntity)
        self.assertEqual(user.entities.description['hashtags'][0].tag, "DevRel")

    def test_user_from_api_response(self):
        result = User.from_api_response(self.sample_api_response)
        
        # Test structure
        self.assertIn('data', result)
        self.assertIn('includes', result)
        self.assertIn('tweets', result['includes'])
        
        # Test users
        self.assertEqual(len(result['data']), 1)
        user = result['data'][0]
        self.assertIsInstance(user, User)
        self.assertEqual(user.id, "2244994945")
        
        # Test included tweets
        self.assertEqual(len(result['includes']['tweets']), 1)
        tweet = result['includes']['tweets'][0]
        self.assertIsInstance(tweet, Tweet)
        self.assertEqual(tweet.id, "1255542774432063488")

if __name__ == '__main__':
    unittest.main() 