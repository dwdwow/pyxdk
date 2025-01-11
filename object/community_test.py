import unittest
from datetime import datetime
from community import Community, CommunityAccess, CommunityJoinPolicy

class TestCommunity(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.community_data = {
            'id': '1234567890',
            'name': 'Python Developers',
            'description': 'A community for Python developers',
            'access': 'Public',
            'join_policy': 'Open',
            'member_count': 1000,
            'created_at': '2023-01-01T12:00:00.000Z'
        }
        
        # Create a community instance for testing
        self.community = Community.from_dict(self.community_data)

    def test_required_attributes(self):
        """Test that required attributes are correctly set"""
        self.assertEqual(self.community.id, '1234567890')
        self.assertEqual(self.community.name, 'Python Developers')
        self.assertEqual(self.community.member_count, 1000)
        
        # Test datetime conversion
        expected_dt = datetime(2023, 1, 1, 12, 0, 0)
        self.assertEqual(self.community.created_at, expected_dt)
        self.assertIsInstance(self.community.created_at, datetime)

    def test_optional_attributes(self):
        """Test optional attributes handling"""
        # Test with description
        self.assertEqual(self.community.description, 'A community for Python developers')
        
        # Test without description
        data_without_description = self.community_data.copy()
        del data_without_description['description']
        community = Community.from_dict(data_without_description)
        self.assertIsNone(community.description)

    def test_access_types(self):
        """Test community access type handling"""
        # Test Public access
        self.assertEqual(self.community.access, CommunityAccess.PUBLIC)
        self.assertEqual(self.community.access.value, 'Public')
        
        # Test Closed access
        closed_data = self.community_data.copy()
        closed_data['access'] = 'Closed'
        closed_community = Community.from_dict(closed_data)
        self.assertEqual(closed_community.access, CommunityAccess.CLOSED)
        self.assertEqual(closed_community.access.value, 'Closed')
        
        # Test invalid access type
        invalid_data = self.community_data.copy()
        invalid_data['access'] = 'Invalid'
        with self.assertRaises(ValueError):
            Community.from_dict(invalid_data)

    def test_join_policies(self):
        """Test community join policy handling"""
        policies = {
            'Open': CommunityJoinPolicy.OPEN,
            'RestrictedJoinRequestsDisabled': CommunityJoinPolicy.RESTRICTED_JOIN_REQUESTS_DISABLED,
            'RestrictedJoinRequestsRequireAdminApproval': CommunityJoinPolicy.RESTRICTED_JOIN_REQUESTS_REQUIRE_ADMIN_APPROVAL,
            'RestrictedJoinRequestsRequireModeratorApproval': CommunityJoinPolicy.RESTRICTED_JOIN_REQUESTS_REQUIRE_MODERATOR_APPROVAL,
            'SuperFollowRequired': CommunityJoinPolicy.SUPER_FOLLOW_REQUIRED
        }
        
        # Test all valid join policies
        for policy_str, policy_enum in policies.items():
            data = self.community_data.copy()
            data['join_policy'] = policy_str
            community = Community.from_dict(data)
            self.assertEqual(community.join_policy, policy_enum)
            self.assertEqual(community.join_policy.value, policy_str)
        
        # Test invalid join policy
        invalid_data = self.community_data.copy()
        invalid_data['join_policy'] = 'Invalid'
        with self.assertRaises(ValueError):
            Community.from_dict(invalid_data)

    def test_minimal_community(self):
        """Test community creation with minimal required data"""
        minimal_data = {
            'id': '1234567890',
            'name': 'Python Developers',
            'access': 'Public',
            'join_policy': 'Open',
            'member_count': 1000,
            'created_at': '2023-01-01T12:00:00.000Z'
        }
        
        community = Community.from_dict(minimal_data)
        
        # Test required fields
        self.assertEqual(community.id, '1234567890')
        self.assertEqual(community.name, 'Python Developers')
        self.assertEqual(community.access, CommunityAccess.PUBLIC)
        self.assertEqual(community.join_policy, CommunityJoinPolicy.OPEN)
        self.assertEqual(community.member_count, 1000)
        self.assertIsInstance(community.created_at, datetime)
        
        # Test optional fields
        self.assertIsNone(community.description)

    def test_missing_required_fields(self):
        """Test that missing required fields raise appropriate errors"""
        required_fields = ['id', 'name', 'access', 'join_policy', 'member_count', 'created_at']
        
        for field in required_fields:
            invalid_data = self.community_data.copy()
            del invalid_data[field]
            with self.assertRaises(KeyError):
                Community.from_dict(invalid_data)

    def test_invalid_datetime_format(self):
        """Test handling of invalid datetime format"""
        invalid_data = self.community_data.copy()
        invalid_data['created_at'] = '2023-01-01'  # Invalid format
        with self.assertRaises(ValueError):
            Community.from_dict(invalid_data)

if __name__ == '__main__':
    unittest.main() 