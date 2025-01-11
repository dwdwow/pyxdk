import unittest
from datetime import datetime
from tweet import (
    Tweet, PublicMetrics, NonPublicMetrics, OrganicMetrics, PromotedMetrics,
    Domain, ContextEntityAnnotation, ContextAnnotation, ReferencedTweet, EditControls,
    Withheld, Entities, EntityAnnotation, Cashtag, Hashtag, Mention, Url
)

class TestTweet(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.tweet_data = {
            'id': '1234567890',
            'text': '#blacklivesmatter $twtr @TwitterDev Check out https://t.co/crkYRdjUB0',
            'author_id': '2244994945',
            'created_at': '2023-01-01T12:00:00.000Z',
            'edit_history_tweet_ids': ['1234567890'],
            'lang': 'en',
            'possibly_sensitive': False,
            'public_metrics': {
                'retweet_count': 10,
                'reply_count': 5,
                'like_count': 20,
                'quote_count': 3
            },
            'entities': {
                'annotations': [{
                    'start': 144,
                    'end': 150,
                    'probability': 0.626,
                    'type': 'Product',
                    'normalized_text': 'Twitter'
                }],
                'cashtags': [{
                    'start': 18,
                    'end': 23,
                    'tag': 'twtr'
                }],
                'hashtags': [{
                    'start': 0,
                    'end': 17,
                    'tag': 'blacklivesmatter'
                }],
                'mentions': [{
                    'start': 24,
                    'end': 35,
                    'tag': 'TwitterDev'
                }],
                'urls': [{
                    'start': 44,
                    'end': 67,
                    'url': 'https://t.co/crkYRdjUB0',
                    'expanded_url': 'https://twitter.com',
                    'display_url': 'twitter.com',
                    'status': '200',
                    'title': 'bird',
                    'description': 'Twitter social media platform',
                    'unwound_url': 'https://twitter.com'
                }]
            },
            'context_annotations': [{
                'domain': {
                    'id': '123',
                    'name': 'Technology',
                    'description': 'Technology and computing'
                },
                'entity': {
                    'id': '456',
                    'name': 'Twitter',
                    'description': 'Social media platform'
                }
            }],
            'referenced_tweets': [{
                'type': 'replied_to',
                'id': '9876543210'
            }],
            'in_reply_to_user_id': '123456789',
            'attachments': {
                'media_keys': ['3_1136048009270239232']
            },
            'conversation_id': '1234567890',
            'edit_controls': {
                'edits_remaining': 5,
                'is_edit_eligible': True,
                'editable_until': '2023-01-01T13:00:00.000Z'
            },
            'non_public_metrics': {
                'impression_count': 100,
                'url_link_clicks': 30,
                'user_profile_clicks': 15
            },
            'organic_metrics': {
                'impression_count': 80,
                'like_count': 15,
                'reply_count': 4,
                'retweet_count': 8,
                'url_link_clicks': 25,
                'user_profile_clicks': 12
            },
            'promoted_metrics': {
                'impression_count': 20,
                'like_count': 5,
                'reply_count': 1,
                'retweet_count': 2,
                'url_link_clicks': 5,
                'user_profile_clicks': 3
            },
            'reply_settings': 'everyone',
            'withheld': {
                'copyright': True,
                'country_codes': ['US', 'GB']
            }
        }
        
        self.tweet = Tweet.from_dict(self.tweet_data)

    def test_required_attributes(self):
        """Test that required attributes are correctly set"""
        self.assertEqual(self.tweet.id, '1234567890')
        self.assertEqual(self.tweet.text, '#blacklivesmatter $twtr @TwitterDev Check out https://t.co/crkYRdjUB0')
        self.assertEqual(self.tweet.author_id, '2244994945')
        self.assertEqual(self.tweet.edit_history_tweet_ids, ['1234567890'])
        
        # Test datetime conversion
        expected_dt = datetime(2023, 1, 1, 12, 0, 0)
        self.assertEqual(self.tweet.created_at, expected_dt)
        self.assertIsInstance(self.tweet.created_at, datetime)

    def test_optional_attributes(self):
        """Test optional attributes handling"""
        self.assertEqual(self.tweet.lang, 'en')
        self.assertFalse(self.tweet.possibly_sensitive)
        self.assertEqual(self.tweet.in_reply_to_user_id, '123456789')
        self.assertEqual(self.tweet.conversation_id, '1234567890')
        self.assertEqual(self.tweet.reply_settings, 'everyone')

    def test_public_metrics(self):
        """Test public metrics handling"""
        self.assertIsInstance(self.tweet.public_metrics, PublicMetrics)
        self.assertEqual(self.tweet.public_metrics.retweet_count, 10)
        self.assertEqual(self.tweet.public_metrics.reply_count, 5)
        self.assertEqual(self.tweet.public_metrics.like_count, 20)
        self.assertEqual(self.tweet.public_metrics.quote_count, 3)

    def test_entities(self):
        """Test entities handling"""
        entities = self.tweet.entities
        self.assertIsInstance(entities, Entities)
        
        # Test annotations
        self.assertEqual(len(entities.annotations), 1)
        annotation = entities.annotations[0]
        self.assertEqual(annotation.normalized_text, 'Twitter')
        self.assertEqual(annotation.type, 'Product')
        
        # Test cashtags
        self.assertEqual(len(entities.cashtags), 1)
        cashtag = entities.cashtags[0]
        self.assertEqual(cashtag.tag, 'twtr')
        
        # Test hashtags
        self.assertEqual(len(entities.hashtags), 1)
        hashtag = entities.hashtags[0]
        self.assertEqual(hashtag.tag, 'blacklivesmatter')
        
        # Test mentions
        self.assertEqual(len(entities.mentions), 1)
        mention = entities.mentions[0]
        self.assertEqual(mention.tag, 'TwitterDev')
        
        # Test urls
        self.assertEqual(len(entities.urls), 1)
        url = entities.urls[0]
        self.assertEqual(url.url, 'https://t.co/crkYRdjUB0')
        self.assertEqual(url.expanded_url, 'https://twitter.com')
        self.assertEqual(url.title, 'bird')

    def test_context_annotations(self):
        """Test context annotations handling"""
        self.assertEqual(len(self.tweet.context_annotations), 1)
        annotation = self.tweet.context_annotations[0]
        
        # Test domain
        self.assertEqual(annotation.domain.id, '123')
        self.assertEqual(annotation.domain.name, 'Technology')
        
        # Test entity
        self.assertEqual(annotation.entity.id, '456')
        self.assertEqual(annotation.entity.name, 'Twitter')

    def test_referenced_tweets(self):
        """Test referenced tweets handling"""
        self.assertEqual(len(self.tweet.referenced_tweets), 1)
        ref_tweet = self.tweet.referenced_tweets[0]
        self.assertEqual(ref_tweet.reference_type, 'replied_to')
        self.assertEqual(ref_tweet.id, '9876543210')

    def test_edit_controls(self):
        """Test edit controls handling"""
        edit_controls = self.tweet.edit_controls
        self.assertEqual(edit_controls.edits_remaining, 5)
        self.assertTrue(edit_controls.is_edit_eligible)
        expected_dt = datetime(2023, 1, 1, 13, 0, 0)
        self.assertEqual(edit_controls.editable_until, expected_dt)

    def test_metrics(self):
        """Test various metrics handling"""
        # Test non-public metrics
        self.assertEqual(self.tweet.non_public_metrics.impression_count, 100)
        self.assertEqual(self.tweet.non_public_metrics.url_link_clicks, 30)
        
        # Test organic metrics
        self.assertEqual(self.tweet.organic_metrics.impression_count, 80)
        self.assertEqual(self.tweet.organic_metrics.like_count, 15)
        
        # Test promoted metrics
        self.assertEqual(self.tweet.promoted_metrics.impression_count, 20)
        self.assertEqual(self.tweet.promoted_metrics.retweet_count, 2)

    def test_withheld(self):
        """Test withheld information handling"""
        self.assertTrue(self.tweet.withheld.copyright)
        self.assertEqual(self.tweet.withheld.country_codes, ['US', 'GB'])

    def test_minimal_tweet(self):
        """Test tweet creation with minimal required data"""
        minimal_data = {
            'id': '1234567890',
            'text': 'Hello, world!',
            'author_id': '2244994945',
            'created_at': '2023-01-01T12:00:00.000Z',
            'edit_history_tweet_ids': ['1234567890'],
            'public_metrics': {
                'retweet_count': 0,
                'reply_count': 0,
                'like_count': 0,
                'quote_count': 0
            }
        }
        
        tweet = Tweet.from_dict(minimal_data)
        
        # Test required fields
        self.assertEqual(tweet.id, '1234567890')
        self.assertEqual(tweet.text, 'Hello, world!')
        self.assertEqual(tweet.author_id, '2244994945')
        self.assertEqual(tweet.edit_history_tweet_ids, ['1234567890'])
        
        # Test that optional fields are None
        self.assertIsNone(tweet.lang)
        self.assertIsNone(tweet.possibly_sensitive)
        self.assertIsNone(tweet.entities)
        self.assertIsNone(tweet.context_annotations)
        self.assertIsNone(tweet.referenced_tweets)
        self.assertIsNone(tweet.in_reply_to_user_id)
        self.assertIsNone(tweet.attachments)
        self.assertIsNone(tweet.conversation_id)
        self.assertIsNone(tweet.edit_controls)
        self.assertIsNone(tweet.non_public_metrics)
        self.assertIsNone(tweet.organic_metrics)
        self.assertIsNone(tweet.promoted_metrics)
        self.assertIsNone(tweet.reply_settings)
        self.assertIsNone(tweet.withheld)

    def test_missing_required_fields(self):
        """Test that missing required fields raise appropriate errors"""
        required_fields = ['id', 'text', 'author_id', 'created_at', 'edit_history_tweet_ids']
        
        for field in required_fields:
            invalid_data = self.tweet_data.copy()
            del invalid_data[field]
            with self.assertRaises(KeyError):
                Tweet.from_dict(invalid_data)

    def test_invalid_datetime_format(self):
        """Test handling of invalid datetime format"""
        invalid_data = self.tweet_data.copy()
        invalid_data['created_at'] = '2023-01-01'  # Invalid format
        with self.assertRaises(ValueError):
            Tweet.from_dict(invalid_data)

if __name__ == '__main__':
    unittest.main() 