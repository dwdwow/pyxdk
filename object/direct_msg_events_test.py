import unittest
from datetime import datetime
from direct_msg_events import DirectMessageEvent, EventType, ReferencedTweet, Attachments

class TestDirectMessageEvent(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.message_data = {
            'id': '1050118621198921728',
            'event_type': 'MessageCreate',
            'text': 'Hello, just you!',
            'sender_id': '906948460078698496',
            'dm_conversation_id': '1584988213961031680',
            'created_at': '2019-06-04T23:12:08.000Z',
            'referenced_tweets': [
                {'id': '1578868150510456833'}
            ],
            'attachments': {
                'media_keys': ['3_1136048009270239232']
            }
        }
        
        self.event = DirectMessageEvent.from_dict(self.message_data)

    def test_basic_attributes(self):
        """Test basic DirectMessageEvent attributes"""
        self.assertEqual(self.event.id, '1050118621198921728')
        self.assertEqual(self.event.event_type, EventType.MESSAGE_CREATE)
        self.assertEqual(self.event.text, 'Hello, just you!')
        self.assertEqual(self.event.sender_id, '906948460078698496')
        self.assertEqual(self.event.dm_conversation_id, '1584988213961031680')
        
        # Test datetime conversion
        expected_dt = datetime(2019, 6, 4, 23, 12, 8)
        self.assertEqual(self.event.created_at, expected_dt)

    def test_referenced_tweets(self):
        """Test referenced tweets handling"""
        self.assertIsInstance(self.event.referenced_tweets, list)
        self.assertEqual(len(self.event.referenced_tweets), 1)
        self.assertIsInstance(self.event.referenced_tweets[0], ReferencedTweet)
        self.assertEqual(self.event.referenced_tweets[0].id, '1578868150510456833')

    def test_attachments(self):
        """Test attachments handling"""
        self.assertIsInstance(self.event.attachments, Attachments)
        self.assertEqual(len(self.event.attachments.media_keys), 1)
        self.assertEqual(self.event.attachments.media_keys[0], '3_1136048009270239232')

    def test_event_types(self):
        """Test different event types"""
        # Test ParticipantsJoin
        join_data = {
            **self.message_data,
            'event_type': 'ParticipantsJoin',
            'text': None,
            'participant_ids': ['906948460078698496']
        }
        join_event = DirectMessageEvent.from_dict(join_data)
        self.assertEqual(join_event.event_type, EventType.PARTICIPANTS_JOIN)
        self.assertEqual(join_event.participant_ids, ['906948460078698496'])
        
        # Test ParticipantsLeave
        leave_data = {
            **self.message_data,
            'event_type': 'ParticipantsLeave',
            'text': None,
            'participant_ids': ['906948460078698496']
        }
        leave_event = DirectMessageEvent.from_dict(leave_data)
        self.assertEqual(leave_event.event_type, EventType.PARTICIPANTS_LEAVE)
        self.assertEqual(leave_event.participant_ids, ['906948460078698496'])

    def test_minimal_event(self):
        """Test event creation with minimal required data"""
        minimal_data = {
            'id': '1050118621198921728',
            'event_type': 'MessageCreate',
            'sender_id': '906948460078698496',
            'dm_conversation_id': '1584988213961031680',
            'created_at': '2019-06-04T23:12:08.000Z'
        }
        
        minimal_event = DirectMessageEvent.from_dict(minimal_data)
        
        # Test required fields
        self.assertEqual(minimal_event.id, '1050118621198921728')
        self.assertEqual(minimal_event.event_type, EventType.MESSAGE_CREATE)
        self.assertEqual(minimal_event.sender_id, '906948460078698496')
        self.assertEqual(minimal_event.dm_conversation_id, '1584988213961031680')
        
        # Test that optional fields are None
        self.assertIsNone(minimal_event.text)
        self.assertIsNone(minimal_event.participant_ids)
        self.assertIsNone(minimal_event.referenced_tweets)
        self.assertIsNone(minimal_event.attachments)

if __name__ == '__main__':
    unittest.main() 