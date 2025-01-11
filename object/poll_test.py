import unittest
from datetime import datetime
from poll import Poll, PollOption

class TestPoll(unittest.TestCase):
    def setUp(self):
        self.sample_poll_data = {
            "id": "1199786642468413448",
            "voting_status": "closed",
            "duration_minutes": 1440,
            "options": [
                {
                    "position": 1,
                    "label": "C Sharp",
                    "votes": 795
                },
                {
                    "position": 2,
                    "label": "C Hashtag",
                    "votes": 156
                }
            ],
            "end_datetime": "2019-11-28T20:26:41.000Z"
        }

        self.sample_api_response = {
            "data": [{
                "text": "C#",
                "id": "1199786642791452673",
                "attachments": {
                    "poll_ids": ["1199786642468413448"]
                }
            }],
            "includes": {
                "polls": [self.sample_poll_data]
            }
        }

    def test_poll_from_dict(self):
        poll = Poll.from_dict(self.sample_poll_data)
        
        # Test basic attributes
        self.assertEqual(poll.id, "1199786642468413448")
        self.assertEqual(poll.voting_status, "closed")
        self.assertEqual(poll.duration_minutes, 1440)
        
        # Test datetime conversion
        self.assertIsInstance(poll.end_datetime, datetime)
        self.assertEqual(poll.end_datetime.year, 2019)
        self.assertEqual(poll.end_datetime.month, 11)
        self.assertEqual(poll.end_datetime.day, 28)
        
        # Test options
        self.assertEqual(len(poll.options), 2)
        self.assertIsInstance(poll.options[0], PollOption)
        
        # Test first option
        first_option = poll.options[0]
        self.assertEqual(first_option.position, 1)
        self.assertEqual(first_option.label, "C Sharp")
        self.assertEqual(first_option.votes, 795)
        
        # Test second option
        second_option = poll.options[1]
        self.assertEqual(second_option.position, 2)
        self.assertEqual(second_option.label, "C Hashtag")
        self.assertEqual(second_option.votes, 156)

    # def test_poll_from_api_response(self):
    #     result = Poll.from_api_response(self.sample_api_response)
        
    #     # Test structure
    #     self.assertIn('includes', result)
    #     self.assertIn('polls', result['includes'])
        
    #     # Test polls
    #     self.assertEqual(len(result['includes']['polls']), 1)
    #     poll = result['includes']['polls'][0]
    #     self.assertIsInstance(poll, Poll)
    #     self.assertEqual(poll.id, "1199786642468413448")
    #     self.assertEqual(len(poll.options), 2)

if __name__ == '__main__':
    unittest.main() 