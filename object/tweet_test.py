import unittest
from datetime import datetime
from tweet import Tweet, PublicMetrics, Entity, Domain, EntityAnnotation, ContextAnnotation, ReferencedTweet

class TestTweet(unittest.TestCase):
    def setUp(self):
        self.sample_tweet_data = {
            "text": "We believe the best future version of our API will come from building it with YOU...",
            "edit_history_tweet_ids": ["1212092628029698048"],
            "lang": "en",
            "in_reply_to_user_id": "2244994945",
            "entities": {
                "urls": [{
                    "start": 222,
                    "end": 245,
                    "url": "https://t.co/yvxdK6aOo2",
                    "expanded_url": "https://twitter.com/LovesNandos/status/1211797914437259264/photo/1",
                    "display_url": "pic.twitter.com/yvxdK6aOo2",
                    "media_key": "16_1211797899316740096"
                }],
                "annotations": [{
                    "start": 42,
                    "end": 44,
                    "probability": 0.5359,
                    "type": "Other",
                    "normalized_text": "API"
                }]
            },
            "author_id": "2244994945",
            "referenced_tweets": [{
                "type": "replied_to",
                "id": "1212092627178287104"
            }],
            "id": "1212092628029698048",
            "public_metrics": {
                "retweet_count": 7,
                "reply_count": 3,
                "like_count": 38,
                "quote_count": 1
            },
            "context_annotations": [{
                "domain": {
                    "id": "29",
                    "name": "Events [Entity Service]",
                    "description": "Real world events. "
                },
                "entity": {
                    "id": "1186637514896920576",
                    "name": " New Years Eve"
                }
            }],
            "created_at": "2019-12-31T19:26:16.000Z",
            "attachments": {
                "media_keys": ["16_1211797899316740096"]
            },
            "possibly_sensitive": False
        }

        self.sample_api_response = {
            "data": [self.sample_tweet_data],
            "includes": {
                "tweets": [
                    {
                        "text": "These launches would not be possible without the feedback...",
                        "edit_history_tweet_ids": ["1212092627178287104"],
                        "lang": "en",
                        "author_id": "2244994945",
                        "id": "1212092627178287104",
                        "created_at": "2019-12-31T19:26:16.000Z",
                        "public_metrics": {
                            "retweet_count": 2,
                            "reply_count": 1,
                            "like_count": 19,
                            "quote_count": 0
                        },
                        "possibly_sensitive": False
                    }
                ]
            }
        }

    def test_tweet_from_dict(self):
        tweet = Tweet.from_dict(self.sample_tweet_data)
        
        # Test basic attributes
        self.assertEqual(tweet.id, "1212092628029698048")
        self.assertEqual(tweet.author_id, "2244994945")
        self.assertEqual(tweet.lang, "en")
        self.assertEqual(tweet.possibly_sensitive, False)
        
        # Test datetime conversion
        self.assertIsInstance(tweet.created_at, datetime)
        self.assertEqual(tweet.created_at.year, 2019)
        self.assertEqual(tweet.created_at.month, 12)
        self.assertEqual(tweet.created_at.day, 31)
        
        # Test public metrics
        self.assertIsInstance(tweet.public_metrics, PublicMetrics)
        self.assertEqual(tweet.public_metrics.retweet_count, 7)
        self.assertEqual(tweet.public_metrics.like_count, 38)
        
        # Test entities
        self.assertIn('urls', tweet.entities)
        self.assertIn('annotations', tweet.entities)
        self.assertIsInstance(tweet.entities['urls'][0], Entity)
        self.assertEqual(tweet.entities['urls'][0].media_key, "16_1211797899316740096")
        
        # Test context annotations
        self.assertIsInstance(tweet.context_annotations[0], ContextAnnotation)
        self.assertEqual(tweet.context_annotations[0].domain.id, "29")
        self.assertEqual(tweet.context_annotations[0].entity.name, " New Years Eve")

    def test_tweet_from_api_response(self):
        result = Tweet.from_api_response(self.sample_api_response)
        
        # Test structure
        self.assertIn('data', result)
        self.assertIn('includes', result)
        self.assertIn('tweets', result['includes'])
        
        # Test main tweets
        self.assertEqual(len(result['data']), 1)
        main_tweet = result['data'][0]
        self.assertIsInstance(main_tweet, Tweet)
        self.assertEqual(main_tweet.id, "1212092628029698048")
        
        # Test included tweets
        self.assertEqual(len(result['includes']['tweets']), 1)
        included_tweet = result['includes']['tweets'][0]
        self.assertIsInstance(included_tweet, Tweet)
        self.assertEqual(included_tweet.id, "1212092627178287104")

if __name__ == '__main__':
    unittest.main() 