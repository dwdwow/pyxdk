import unittest
from datetime import datetime
from poll import Poll, PollOption, VotingStatus

class TestPoll(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.poll_data = {
            'id': '1199786642791452673',
            'options': [
                {
                    'position': 1,
                    'label': 'C Sharp',
                    'votes': 795
                },
                {
                    'position': 2,
                    'label': 'C Hashtag',
                    'votes': 156
                }
            ],
            'duration_minutes': 1440,
            'end_datetime': '2019-11-28T20:26:41.000Z',
            'voting_status': 'closed'
        }
        
        self.poll = Poll.from_dict(self.poll_data)

    def test_basic_attributes(self):
        """Test basic Poll attributes"""
        self.assertEqual(self.poll.id, '1199786642791452673')
        self.assertEqual(self.poll.duration_minutes, 1440)
        self.assertEqual(self.poll.voting_status, VotingStatus.CLOSED)

    def test_options(self):
        """Test poll options"""
        self.assertEqual(len(self.poll.options), 2)
        
        # Test first option
        option1 = self.poll.options[0]
        self.assertIsInstance(option1, PollOption)
        self.assertEqual(option1.position, 1)
        self.assertEqual(option1.label, 'C Sharp')
        self.assertEqual(option1.votes, 795)
        
        # Test second option
        option2 = self.poll.options[1]
        self.assertIsInstance(option2, PollOption)
        self.assertEqual(option2.position, 2)
        self.assertEqual(option2.label, 'C Hashtag')
        self.assertEqual(option2.votes, 156)

    def test_end_datetime(self):
        """Test datetime conversion"""
        expected_datetime = datetime(2019, 11, 28, 20, 26, 41)
        self.assertEqual(self.poll.end_datetime, expected_datetime)

    def test_voting_status(self):
        """Test different voting statuses"""
        # Test closed poll
        self.assertEqual(self.poll.voting_status, VotingStatus.CLOSED)
        
        # Test open poll
        open_poll_data = {
            **self.poll_data,
            'voting_status': 'open'
        }
        open_poll = Poll.from_dict(open_poll_data)
        self.assertEqual(open_poll.voting_status, VotingStatus.OPEN)

    def test_minimal_poll(self):
        """Test poll creation with minimal required data"""
        minimal_data = {
            'id': '1199786642791452673',
            'options': [
                {
                    'position': 1,
                    'label': 'Yes',
                    'votes': 100
                },
                {
                    'position': 2,
                    'label': 'No',
                    'votes': 50
                }
            ],
            'voting_status': 'open'
        }
        
        minimal_poll = Poll.from_dict(minimal_data)
        
        # Test required fields
        self.assertEqual(minimal_poll.id, '1199786642791452673')
        self.assertEqual(len(minimal_poll.options), 2)
        self.assertEqual(minimal_poll.voting_status, VotingStatus.OPEN)
        
        # Test that optional fields are None
        self.assertIsNone(minimal_poll.duration_minutes)
        self.assertIsNone(minimal_poll.end_datetime)

    def test_total_votes(self):
        """Test calculation of total votes"""
        total_votes = sum(option.votes for option in self.poll.options)
        self.assertEqual(total_votes, 951)  # 795 + 156

if __name__ == '__main__':
    unittest.main() 