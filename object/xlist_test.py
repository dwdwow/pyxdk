import unittest
from datetime import datetime
from object.xlist import List

class TestList(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.list_data = {
            'id': '2244994945',
            'name': 'Twitter Lists',
            'owner_id': '1255542774432063488',
            'private': False,
            'follower_count': 198,
            'member_count': 60,
            'created_at': '2013-12-14T04:35:55.000Z',
            'description': 'People that are active members of the Bay area cycling community on Twitter.'
        }
        
        self.list = List.from_dict(self.list_data)

    def test_basic_attributes(self):
        """Test basic List attributes"""
        self.assertEqual(self.list.id, '2244994945')
        self.assertEqual(self.list.name, 'Twitter Lists')
        self.assertEqual(self.list.owner_id, '1255542774432063488')
        self.assertFalse(self.list.private)
        self.assertEqual(self.list.follower_count, 198)
        self.assertEqual(self.list.member_count, 60)
        self.assertEqual(
            self.list.description,
            'People that are active members of the Bay area cycling community on Twitter.'
        )

    def test_created_at(self):
        """Test datetime conversion"""
        expected_datetime = datetime(2013, 12, 14, 4, 35, 55)
        self.assertEqual(self.list.created_at, expected_datetime)

    def test_minimal_list(self):
        """Test list creation with minimal required data"""
        minimal_data = {
            'id': '2244994945',
            'name': 'Minimal List',
            'owner_id': '1255542774432063488',
            'private': True,
            'follower_count': 0,
            'member_count': 0
        }
        
        minimal_list = List.from_dict(minimal_data)
        
        # Test required fields
        self.assertEqual(minimal_list.id, '2244994945')
        self.assertEqual(minimal_list.name, 'Minimal List')
        self.assertEqual(minimal_list.owner_id, '1255542774432063488')
        self.assertTrue(minimal_list.private)
        self.assertEqual(minimal_list.follower_count, 0)
        self.assertEqual(minimal_list.member_count, 0)
        
        # Test that optional fields are None
        self.assertIsNone(minimal_list.created_at)
        self.assertIsNone(minimal_list.description)

    def test_private_list(self):
        """Test private list creation"""
        private_data = {
            **self.list_data,
            'private': True
        }
        private_list = List.from_dict(private_data)
        self.assertTrue(private_list.private)

if __name__ == '__main__':
    unittest.main() 