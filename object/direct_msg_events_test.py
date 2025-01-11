import unittest
from datetime import datetime
from direct_msg_events import DirectMessageEvent, ReferencedTweet
from user import User
from tweet import Tweet

class TestDirectMessageEvent(unittest.TestCase):
    def setUp(self):
        self.sample_dm_data = {
            "id": "1585047616894574596",
            "sender_id": "944480690",
            "text": "Hello, just you!",
            "created_at": "2022-10-25T23:16:15.000Z",
            "event_type": "MessageCreate",
            "dm_conversation_id": "944480690-906948460078698496"
        }

        self.sample_dm_with_tweet = {
            "id": "1581048670673260549",
            "sender_id": "944480690",
            "text": "Simple Tweet link: https://t.co/IYFbRIdXHg",
            "referenced_tweets": [{
                "id": "1578900353814519810"
            }],
            "created_at": "2022-10-14T22:25:52.000Z",
            "event_type": "MessageCreate",
            "dm_conversation_id": "944480690-906948460078698496"
        }

        self.sample_api_response = {
            "data": [
                self.sample_dm_data,
                self.sample_dm_with_tweet
            ],
            "includes": {
                "users": [{
                    "name": "API Demos",
                    "description": "Hosting TwitterDev integrations...",
                    "id": "944480690",
                    "username": "FloodSocial"
                }],
                "tweets": [{
                    "text": "Feeling kind of bad...",
                    "id": "1578900353814519810",
                    "created_at": "2022-10-09T00:09:13.000Z",
                    "author_id": "944480690",
                    "edit_history_tweet_ids": ["1578900353814519810"]
                }]
            },
            "meta": {
                "result_count": 2,
                "next_token": "18LAA581J5II7LA00C00ZZZZ"
            }
        }

    def test_dm_from_dict(self):
        dm = DirectMessageEvent.from_dict(self.sample_dm_data)
        
        # Test basic attributes
        self.assertEqual(dm.id, "1585047616894574596")
        self.assertEqual(dm.sender_id, "944480690")
        self.assertEqual(dm.text, "Hello, just you!")
        self.assertEqual(dm.event_type, "MessageCreate")
        self.assertEqual(
            dm.dm_conversation_id,
            "944480690-906948460078698496"
        )
        
        # Test datetime conversion
        self.assertIsInstance(dm.created_at, datetime)
        self.assertEqual(dm.created_at.year, 2022)
        self.assertEqual(dm.created_at.month, 10)
        self.assertEqual(dm.created_at.day, 25)
        
        # Test no referenced tweets
        self.assertIsNone(dm.referenced_tweets)

    def test_dm_with_referenced_tweet(self):
        dm = DirectMessageEvent.from_dict(self.sample_dm_with_tweet)
        
        # Test referenced tweets
        self.assertIsNotNone(dm.referenced_tweets)
        self.assertEqual(len(dm.referenced_tweets), 1)
        self.assertIsInstance(dm.referenced_tweets[0], ReferencedTweet)
        self.assertEqual(dm.referenced_tweets[0].id, "1578900353814519810")

    def test_dm_from_api_response(self):
        result = DirectMessageEvent.from_api_response(self.sample_api_response)
        
        # Test structure
        self.assertIn('data', result)
        self.assertIn('includes', result)
        self.assertIn('meta', result)
        self.assertIn('users', result['includes'])
        self.assertIn('tweets', result['includes'])
        
        # Test DM events
        self.assertEqual(len(result['data']), 2)
        dm = result['data'][0]
        self.assertIsInstance(dm, DirectMessageEvent)
        self.assertEqual(dm.id, "1585047616894574596")
        
        # Test included users
        self.assertEqual(len(result['includes']['users']), 1)
        user = result['includes']['users'][0]
        self.assertIsInstance(user, User)
        self.assertEqual(user.id, "944480690")
        
        # Test included tweets
        self.assertEqual(len(result['includes']['tweets']), 1)
        tweet = result['includes']['tweets'][0]
        self.assertIsInstance(tweet, Tweet)
        self.assertEqual(tweet.id, "1578900353814519810")
        
        # Test meta data
        self.assertEqual(result['meta']['result_count'], 2)
        self.assertEqual(
            result['meta']['next_token'],
            "18LAA581J5II7LA00C00ZZZZ"
        )

if __name__ == '__main__':
    unittest.main() 