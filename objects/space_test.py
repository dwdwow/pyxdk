import unittest
from datetime import datetime
from space import Space, SpaceState

class TestSpace(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.space_data = {
            'id': '1DXxyRYNejbKM',
            'state': 'live',
            'created_at': '2023-01-01T12:00:00.000Z',
            'ended_at': '2023-01-01T13:00:00.000Z',
            'host_ids': ['123456789', '987654321'],
            'lang': 'en',
            'is_ticketed': False,
            'invited_user_ids': ['111111111', '222222222'],
            'participant_count': 100,
            'subscriber_count': 50,
            'scheduled_start': '2023-01-01T11:45:00.000Z',
            'speaker_ids': ['123456789', '333333333'],
            'started_at': '2023-01-01T12:00:00.000Z',
            'title': 'Python Programming Space',
            'topic_ids': ['848282', '848283'],
            'updated_at': '2023-01-01T13:00:00.000Z'
        }
        
        self.space = Space.from_dict(self.space_data)

    def test_required_attributes(self):
        """Test that required attributes are correctly set"""
        self.assertEqual(self.space.id, '1DXxyRYNejbKM')
        self.assertEqual(self.space.state, SpaceState.LIVE)
        
        # Test datetime conversions
        expected_created = datetime(2023, 1, 1, 12, 0, 0)
        self.assertEqual(self.space.created_at, expected_created)
        
        expected_ended = datetime(2023, 1, 1, 13, 0, 0)
        self.assertEqual(self.space.ended_at, expected_ended)

    def test_optional_attributes(self):
        """Test optional attributes handling"""
        self.assertEqual(self.space.host_ids, ['123456789', '987654321'])
        self.assertEqual(self.space.lang, 'en')
        self.assertFalse(self.space.is_ticketed)
        self.assertEqual(self.space.invited_user_ids, ['111111111', '222222222'])
        self.assertEqual(self.space.participant_count, 100)
        self.assertEqual(self.space.subscriber_count, 50)
        self.assertEqual(self.space.speaker_ids, ['123456789', '333333333'])
        self.assertEqual(self.space.title, 'Python Programming Space')
        self.assertEqual(self.space.topic_ids, ['848282', '848283'])

    def test_datetime_fields(self):
        """Test all datetime field conversions"""
        expected_times = {
            'created_at': datetime(2023, 1, 1, 12, 0, 0),
            'ended_at': datetime(2023, 1, 1, 13, 0, 0),
            'scheduled_start': datetime(2023, 1, 1, 11, 45, 0),
            'started_at': datetime(2023, 1, 1, 12, 0, 0),
            'updated_at': datetime(2023, 1, 1, 13, 0, 0)
        }
        
        for field, expected_time in expected_times.items():
            self.assertEqual(getattr(self.space, field), expected_time)

    def test_space_states(self):
        """Test different space states"""
        test_states = {
            'scheduled': SpaceState.SCHEDULED,
            'live': SpaceState.LIVE,
            'ended': SpaceState.ENDED
        }
        
        for state_str, state_enum in test_states.items():
            data = self.space_data.copy()
            data['state'] = state_str
            space = Space.from_dict(data)
            self.assertEqual(space.state, state_enum)

    def test_minimal_space(self):
        """Test space creation with minimal required data"""
        minimal_data = {
            'id': '1DXxyRYNejbKM',
            'state': 'live',
            'created_at': '2023-01-01T12:00:00.000Z'
        }
        
        space = Space.from_dict(minimal_data)
        
        # Test required fields
        self.assertEqual(space.id, '1DXxyRYNejbKM')
        self.assertEqual(space.state, SpaceState.LIVE)
        self.assertEqual(space.created_at, datetime(2023, 1, 1, 12, 0, 0))
        
        # Test that optional fields are None
        self.assertIsNone(space.ended_at)
        self.assertIsNone(space.host_ids)
        self.assertIsNone(space.lang)
        self.assertIsNone(space.is_ticketed)
        self.assertIsNone(space.invited_user_ids)
        self.assertIsNone(space.participant_count)
        self.assertIsNone(space.subscriber_count)
        self.assertIsNone(space.scheduled_start)
        self.assertIsNone(space.speaker_ids)
        self.assertIsNone(space.started_at)
        self.assertIsNone(space.title)
        self.assertIsNone(space.topic_ids)
        self.assertIsNone(space.updated_at)

    def test_missing_required_fields(self):
        """Test that missing required fields raise appropriate errors"""
        required_fields = ['id', 'state', 'created_at']
        
        for field in required_fields:
            invalid_data = self.space_data.copy()
            del invalid_data[field]
            with self.assertRaises(KeyError):
                Space.from_dict(invalid_data)

    def test_invalid_state(self):
        """Test handling of invalid space state"""
        invalid_data = self.space_data.copy()
        invalid_data['state'] = 'invalid_state'
        with self.assertRaises(ValueError):
            Space.from_dict(invalid_data)

    def test_invalid_datetime_format(self):
        """Test handling of invalid datetime format"""
        datetime_fields = [
            'created_at', 'ended_at', 'scheduled_start', 
            'started_at', 'updated_at'
        ]
        
        for field in datetime_fields:
            invalid_data = self.space_data.copy()
            invalid_data[field] = '2023-01-01'  # Invalid format
            if field == 'created_at':
                # created_at is required, should raise ValueError
                with self.assertRaises(ValueError):
                    Space.from_dict(invalid_data)
            else:
                # Other datetime fields are optional, should be set to None
                space = Space.from_dict(invalid_data)
                self.assertIsNone(getattr(space, field))

    def test_participant_counts(self):
        """Test participant and subscriber count handling"""
        test_counts = [
            {'participant_count': 0, 'subscriber_count': 0},
            {'participant_count': 100, 'subscriber_count': 50},
            {'participant_count': 1000000, 'subscriber_count': 500000}
        ]
        
        for counts in test_counts:
            data = self.space_data.copy()
            data.update(counts)
            space = Space.from_dict(data)
            self.assertEqual(space.participant_count, counts['participant_count'])
            self.assertEqual(space.subscriber_count, counts['subscriber_count'])

if __name__ == '__main__':
    unittest.main() 