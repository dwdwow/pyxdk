import unittest
from errors import Errors

class TestErrors(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.error_data = {
            'client_id': '101010101',
            'required_enrollment': 'Standard Basic',
            'registration_url': 'https://developer.twitter.com/en/account',
            'title': 'Client Forbidden',
            'detail': 'This request must be made using an approved developer account that is enrolled in the requested endpoint. Learn more by visiting our documentation.',
            'reason': 'client-not-enrolled',
            'type': 'https://api.x.com/2/problems/client-forbidden'
        }
        
        self.error = Errors.from_dict(self.error_data)

    def test_complete_error(self):
        """Test error with all fields present"""
        self.assertEqual(self.error.client_id, '101010101')
        self.assertEqual(self.error.required_enrollment, 'Standard Basic')
        self.assertEqual(self.error.registration_url, 'https://developer.twitter.com/en/account')
        self.assertEqual(self.error.title, 'Client Forbidden')
        self.assertEqual(
            self.error.detail,
            'This request must be made using an approved developer account that is enrolled in the requested endpoint. Learn more by visiting our documentation.'
        )
        self.assertEqual(self.error.reason, 'client-not-enrolled')
        self.assertEqual(self.error.error_type, 'https://api.x.com/2/problems/client-forbidden')

    def test_empty_error(self):
        """Test error creation with empty data"""
        empty_error = Errors.from_dict({})
        
        # All fields should be None
        self.assertIsNone(empty_error.client_id)
        self.assertIsNone(empty_error.required_enrollment)
        self.assertIsNone(empty_error.registration_url)
        self.assertIsNone(empty_error.title)
        self.assertIsNone(empty_error.detail)
        self.assertIsNone(empty_error.reason)
        self.assertIsNone(empty_error.error_type)

    def test_partial_error(self):
        """Test error with partial data"""
        test_cases = [
            # Only client information
            {
                'data': {
                    'client_id': '101010101',
                    'required_enrollment': 'Standard Basic'
                },
                'expected_present': ['client_id', 'required_enrollment'],
                'expected_none': ['registration_url', 'title', 'detail', 'reason', 'error_type']
            },
            # Only error information
            {
                'data': {
                    'title': 'Client Forbidden',
                    'detail': 'Access forbidden',
                    'reason': 'client-not-enrolled'
                },
                'expected_present': ['title', 'detail', 'reason'],
                'expected_none': ['client_id', 'required_enrollment', 'registration_url', 'error_type']
            }
        ]
        
        for test_case in test_cases:
            error = Errors.from_dict(test_case['data'])
            
            # Check fields that should be present
            for field in test_case['expected_present']:
                self.assertEqual(getattr(error, field), test_case['data'][field])
            
            # Check fields that should be None
            for field in test_case['expected_none']:
                self.assertIsNone(getattr(error, field))

    def test_common_error_patterns(self):
        """Test common Twitter API error patterns"""
        error_patterns = [
            # Client forbidden error
            {
                'client_id': '101010101',
                'required_enrollment': 'Standard Basic',
                'title': 'Client Forbidden',
                'type': 'https://api.x.com/2/problems/client-forbidden'
            },
            # Authentication error
            {
                'title': 'Authentication Required',
                'detail': 'Authentication credentials were missing or incorrect',
                'type': 'https://api.x.com/2/problems/authentication-error'
            },
            # Rate limit error
            {
                'title': 'Rate Limit Exceeded',
                'detail': 'You have exceeded the rate limit',
                'type': 'https://api.x.com/2/problems/rate-limit'
            }
        ]
        
        for pattern in error_patterns:
            error = Errors.from_dict(pattern)
            for key, value in pattern.items():
                # Convert 'type' to 'error_type' when checking
                field = 'error_type' if key == 'type' else key
                self.assertEqual(getattr(error, field), value)

if __name__ == '__main__':
    unittest.main() 