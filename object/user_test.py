import unittest
from datetime import datetime
from user import (
    User, UrlEntity, HashtagEntity, MentionEntity, CashtagEntity,
    UserEntities, UserPublicMetrics, Withheld
)

class TestUser(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.user_data = {
            'id': '2244994945',
            'name': 'Twitter Dev',
            'username': 'TwitterDev',
            'created_at': '2013-12-14T04:35:55.000Z',
            'description': 'The voice of the X Dev team and your official source for updates, news, and events, related to the X API. #DevRel',
            'protected': False,
            'verified': True,
            'entities': {
                'url': {
                    'urls': [{
                        'start': 0,
                        'end': 23,
                        'url': 'https://t.co/3ZX3TNiZCY',
                        'expanded_url': '/content/developer-twitter/en/community',
                        'display_url': 'developer.twitter.com/en/community'
                    }]
                },
                'description': {
                    'urls': [{
                        'start': 0,
                        'end': 23,
                        'url': 'https://t.co/3ZX3TNiZCY',
                        'expanded_url': '/content/developer-twitter/en/community',
                        'display_url': 'developer.twitter.com/en/community'
                    }],
                    'hashtags': [{
                        'start': 23,
                        'end': 30,
                        'tag': 'DevRel'
                    }],
                    'mentions': [{
                        'start': 0,
                        'end': 10,
                        'tag': 'TwitterDev'
                    }],
                    'cashtags': [{
                        'start': 12,
                        'end': 16,
                        'tag': 'twtr'
                    }]
                }
            },
            'public_metrics': {
                'followers_count': 507902,
                'following_count': 1863,
                'tweet_count': 3561,
                'listed_count': 1550
            },
            'url': 'https://t.co/3ZX3TNiZCY',
            'location': '127.0.0.1',
            'pinned_tweet_id': '1255542774432063488',
            'profile_image_url': 'https://pbs.twimg.com/profile_images/1267175364003901441/tBZNFAgA_normal.jpg',
            'connection_status': [
                'follow_request_received',
                'follow_request_sent',
                'blocking',
                'followed_by',
                'following',
                'muting'
            ],
            'withheld': {
                'country_codes': ['US', 'EU'],
                'scope': 'user'
            }
        }
        
        self.user = User.from_dict(self.user_data)

    def test_basic_attributes(self):
        """Test basic User attributes"""
        self.assertEqual(self.user.id, '2244994945')
        self.assertEqual(self.user.name, 'Twitter Dev')
        self.assertEqual(self.user.username, 'TwitterDev')
        self.assertEqual(
            self.user.description,
            'The voice of the X Dev team and your official source for updates, news, and events, related to the X API. #DevRel'
        )
        self.assertFalse(self.user.protected)
        self.assertTrue(self.user.verified)

    def test_created_at(self):
        """Test datetime conversion"""
        expected_datetime = datetime(2013, 12, 14, 4, 35, 55)
        self.assertEqual(self.user.created_at, expected_datetime)

    def test_public_metrics(self):
        """Test public metrics conversion"""
        self.assertIsInstance(self.user.public_metrics, UserPublicMetrics)
        self.assertEqual(self.user.public_metrics.followers_count, 507902)
        self.assertEqual(self.user.public_metrics.following_count, 1863)
        self.assertEqual(self.user.public_metrics.tweet_count, 3561)
        self.assertEqual(self.user.public_metrics.listed_count, 1550)

    def test_entities(self):
        """Test entities conversion"""
        self.assertIsInstance(self.user.entities, UserEntities)
        
        # Test URL entities
        self.assertIn('urls', self.user.entities.url)
        url_entity = self.user.entities.url['urls'][0]
        self.assertIsInstance(url_entity, UrlEntity)
        self.assertEqual(url_entity.url, 'https://t.co/3ZX3TNiZCY')
        self.assertEqual(url_entity.expanded_url, '/content/developer-twitter/en/community')
        self.assertEqual(url_entity.display_url, 'developer.twitter.com/en/community')
        
        # Test description entities
        desc_entities = self.user.entities.description
        
        # Test URLs in description
        self.assertIn('urls', desc_entities)
        desc_url = desc_entities['urls'][0]
        self.assertIsInstance(desc_url, UrlEntity)
        self.assertEqual(desc_url.url, 'https://t.co/3ZX3TNiZCY')
        
        # Test hashtags in description
        self.assertIn('hashtags', desc_entities)
        hashtag = desc_entities['hashtags'][0]
        self.assertIsInstance(hashtag, HashtagEntity)
        self.assertEqual(hashtag.tag, 'DevRel')
        
        # Test mentions in description
        self.assertIn('mentions', desc_entities)
        mention = desc_entities['mentions'][0]
        self.assertIsInstance(mention, MentionEntity)
        self.assertEqual(mention.tag, 'TwitterDev')
        
        # Test cashtags in description
        self.assertIn('cashtags', desc_entities)
        cashtag = desc_entities['cashtags'][0]
        self.assertIsInstance(cashtag, CashtagEntity)
        self.assertEqual(cashtag.tag, 'twtr')

    def test_optional_fields(self):
        """Test optional fields"""
        self.assertEqual(self.user.url, 'https://t.co/3ZX3TNiZCY')
        self.assertEqual(self.user.location, '127.0.0.1')
        self.assertEqual(self.user.pinned_tweet_id, '1255542774432063488')
        self.assertEqual(
            self.user.profile_image_url,
            'https://pbs.twimg.com/profile_images/1267175364003901441/tBZNFAgA_normal.jpg'
        )

    def test_connection_status(self):
        """Test connection status array"""
        expected_statuses = {
            'follow_request_received',
            'follow_request_sent',
            'blocking',
            'followed_by',
            'following',
            'muting'
        }
        self.assertEqual(set(self.user.connection_status), expected_statuses)

    def test_withheld(self):
        """Test withheld information"""
        self.assertIsInstance(self.user.withheld, Withheld)
        self.assertEqual(self.user.withheld.country_codes, ['US', 'EU'])
        self.assertEqual(self.user.withheld.scope, 'user')

    def test_minimal_user(self):
        """Test user creation with minimal required data"""
        minimal_data = {
            'id': '123456',
            'name': 'Minimal User',
            'username': 'minimal',
            'created_at': '2023-01-01T12:00:00.000Z',
            'description': 'A minimal user profile',
            'protected': False,
            'verified': False,
            'entities': {},
            'public_metrics': {
                'followers_count': 0,
                'following_count': 0,
                'tweet_count': 0,
                'listed_count': 0
            }
        }
        
        minimal_user = User.from_dict(minimal_data)
        
        # Test required fields
        self.assertEqual(minimal_user.id, '123456')
        self.assertEqual(minimal_user.name, 'Minimal User')
        self.assertEqual(minimal_user.username, 'minimal')
        
        # Test that optional fields are None
        self.assertIsNone(minimal_user.url)
        self.assertIsNone(minimal_user.location)
        self.assertIsNone(minimal_user.pinned_tweet_id)
        self.assertIsNone(minimal_user.profile_image_url)
        self.assertIsNone(minimal_user.connection_status)
        self.assertIsNone(minimal_user.withheld)
        
        # Test empty entities
        self.assertIsNone(minimal_user.entities.url)
        self.assertIsNone(minimal_user.entities.description)

if __name__ == '__main__':
    unittest.main() 