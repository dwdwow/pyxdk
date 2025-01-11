import unittest
from datetime import datetime
from space import Space, SpaceState

class TestSpace(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.space_data = {
            'id': '1zqKVXPQhvZJB',
            'state': 'live',
            'title': 'Say hello to the Space data object!',
            'created_at': '2021-07-04T23:12:08.000Z',
            'host_ids': ['2244994945', '6253282'],
            'participant_count': 420,
            'lang': 'en',
            'is_ticketed': False,
            'invited_user_ids': ['2244994945', '6253282'],
            'speaker_ids': ['2244994945', '6253282'],
            'topic_ids': ['1234', '5678'],
            'subscriber_count': 36,
            'scheduled_start': '2021-07-14T08:00:00.000Z',
            'started_at': '2021-07-14T08:00:12.000Z',
            'ended_at': '2021-07-14T09:00:00.000Z',
            'updated_at': '2021-07-11T14:44:44.000Z'
        }
        
        self.space = Space.from_dict(self.space_data)

    def test_basic_attributes(self):
        """Test basic Space attributes"""
        self.assertEqual(self.space.id, '1zqKVXPQhvZJB')
        self.assertEqual(self.space.state, SpaceState.LIVE)
        self.assertEqual(self.space.title, 'Say hello to the Space data object!')
        self.assertEqual(self.space.participant_count, 420)
        self.assertEqual(self.space.lang, 'en')
        self.assertFalse(self.space.is_ticketed)

    def test_datetime_fields(self):
        """Test datetime conversions"""
        self.assertEqual(
            self.space.created_at,
            datetime(2021, 7, 4, 23, 12, 8)
        )
        self.assertEqual(
            self.space.scheduled_start,
            datetime(2021, 7, 14, 8, 0, 0)
        )
        self.assertEqual(
            self.space.started_at,
            datetime(2021, 7, 14, 8, 0, 12)
        )
        self.assertEqual(
            self.space.ended_at,
            datetime(2021, 7, 14, 9, 0, 0)
        )
        self.assertEqual(
            self.space.updated_at,
            datetime(2021, 7, 11, 14, 44, 44)
        )

    def test_array_fields(self):
        """Test array fields"""
        self.assertEqual(self.space.host_ids, ['2244994945', '6253282'])
        self.assertEqual(self.space.invited_user_ids, ['2244994945', '6253282'])
        self.assertEqual(self.space.speaker_ids, ['2244994945', '6253282'])
        self.assertEqual(self.space.topic_ids, ['1234', '5678'])

    def test_subscriber_count(self):
        """Test subscriber count"""
        self.assertEqual(self.space.subscriber_count, 36)

    def test_minimal_space(self):
        """Test space creation with minimal required data"""
        minimal_data = {
            'id': '1zqKVXPQhvZJB',
            'state': 'scheduled',
            'title': 'Minimal Space',
            'host_ids': ['2244994945'],
            'participant_count': 0
        }
        
        minimal_space = Space.from_dict(minimal_data)
        
        # Test required fields
        self.assertEqual(minimal_space.id, '1zqKVXPQhvZJB')
        self.assertEqual(minimal_space.state, SpaceState.SCHEDULED)
        self.assertEqual(minimal_space.title, 'Minimal Space')
        self.assertEqual(minimal_space.host_ids, ['2244994945'])
        self.assertEqual(minimal_space.participant_count, 0)
        
        # Test that optional fields are None
        self.assertIsNone(minimal_space.created_at)
        self.assertIsNone(minimal_space.ended_at)
        self.assertIsNone(minimal_space.started_at)
        self.assertIsNone(minimal_space.scheduled_start)
        self.assertIsNone(minimal_space.updated_at)
        self.assertIsNone(minimal_space.invited_user_ids)
        self.assertIsNone(minimal_space.speaker_ids)
        self.assertIsNone(minimal_space.topic_ids)
        self.assertIsNone(minimal_space.lang)
        self.assertIsNone(minimal_space.subscriber_count)
        self.assertFalse(minimal_space.is_ticketed)

    def test_space_states(self):
        """Test different space states"""
        # Test live space
        live_data = {'state': 'live', **minimal_data}
        live_space = Space.from_dict(live_data)
        self.assertEqual(live_space.state, SpaceState.LIVE)
        
        # Test scheduled space
        scheduled_data = {'state': 'scheduled', **minimal_data}
        scheduled_space = Space.from_dict(scheduled_data)
        self.assertEqual(scheduled_space.state, SpaceState.SCHEDULED)
        
        # Test ended space
        ended_data = {'state': 'ended', **minimal_data}
        ended_space = Space.from_dict(ended_data)
        self.assertEqual(ended_space.state, SpaceState.ENDED)

if __name__ == '__main__':
    unittest.main() 