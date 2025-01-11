import unittest
from annotation import Annotation, AnnotationType

class TestAnnotation(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.annotation_data = {
            'start': 144,
            'end': 150,
            'probability': 0.626,
            'type': 'Product',
            'normalized_text': 'Twitter'
        }
        
        self.annotation = Annotation.from_dict(self.annotation_data)

    def test_basic_attributes(self):
        """Test that basic attributes are correctly set"""
        self.assertEqual(self.annotation.start, 144)
        self.assertEqual(self.annotation.end, 150)
        self.assertEqual(self.annotation.probability, 0.626)
        self.assertEqual(self.annotation.annotation_type, AnnotationType.PRODUCT)
        self.assertEqual(self.annotation.normalized_text, 'Twitter')

    def test_annotation_types(self):
        """Test different annotation types"""
        test_cases = [
            # Person examples
            {
                'type': 'Person',
                'normalized_text': 'Barack Obama',
                'expected_type': AnnotationType.PERSON
            },
            {
                'type': 'Person',
                'normalized_text': 'George W. Bush',
                'expected_type': AnnotationType.PERSON
            },
            # Place examples
            {
                'type': 'Place',
                'normalized_text': 'Detroit',
                'expected_type': AnnotationType.PLACE
            },
            {
                'type': 'Place',
                'normalized_text': 'San Francisco, California',
                'expected_type': AnnotationType.PLACE
            },
            # Product examples
            {
                'type': 'Product',
                'normalized_text': 'Mountain Dew',
                'expected_type': AnnotationType.PRODUCT
            },
            {
                'type': 'Product',
                'normalized_text': 'Mozilla Firefox',
                'expected_type': AnnotationType.PRODUCT
            },
            # Organization examples
            {
                'type': 'Organization',
                'normalized_text': 'Chicago White Sox',
                'expected_type': AnnotationType.ORGANIZATION
            },
            {
                'type': 'Organization',
                'normalized_text': 'IBM',
                'expected_type': AnnotationType.ORGANIZATION
            },
            # Other examples
            {
                'type': 'Other',
                'normalized_text': 'Diabetes',
                'expected_type': AnnotationType.OTHER
            },
            {
                'type': 'Other',
                'normalized_text': 'Super Bowl 50',
                'expected_type': AnnotationType.OTHER
            }
        ]
        
        for test_case in test_cases:
            data = {
                'type': test_case['type'],
                'normalized_text': test_case['normalized_text']
            }
            
            annotation = Annotation.from_dict(data)
            self.assertEqual(annotation.annotation_type, test_case['expected_type'])
            self.assertEqual(annotation.normalized_text, test_case['normalized_text'])
            # Optional fields should be None
            self.assertIsNone(annotation.start)
            self.assertIsNone(annotation.end)
            self.assertIsNone(annotation.probability)

    def test_invalid_type(self):
        """Test handling of invalid annotation type"""
        invalid_data = {'type': 'InvalidType'}
        with self.assertRaises(ValueError):
            Annotation.from_dict(invalid_data)

    def test_optional_fields(self):
        """Test handling of optional fields"""
        # Test with empty data
        empty_annotation = Annotation.from_dict({})
        self.assertIsNone(empty_annotation.start)
        self.assertIsNone(empty_annotation.end)
        self.assertIsNone(empty_annotation.probability)
        self.assertIsNone(empty_annotation.annotation_type)
        self.assertIsNone(empty_annotation.normalized_text)
        
        # Test with partial data
        test_cases = [
            # Only start and end
            {
                'data': {'start': 0, 'end': 5},
                'expected_present': ['start', 'end'],
                'expected_none': ['probability', 'annotation_type', 'normalized_text']
            },
            # Only type and normalized_text
            {
                'data': {'type': 'Person', 'normalized_text': 'John'},
                'expected_present': ['annotation_type', 'normalized_text'],
                'expected_none': ['start', 'end', 'probability']
            },
            # Only probability
            {
                'data': {'probability': 0.95},
                'expected_present': ['probability'],
                'expected_none': ['start', 'end', 'annotation_type', 'normalized_text']
            }
        ]
        
        for test_case in test_cases:
            annotation = Annotation.from_dict(test_case['data'])
            
            # Check fields that should be present
            for field in test_case['expected_present']:
                if field == 'annotation_type' and 'type' in test_case['data']:
                    self.assertEqual(annotation.annotation_type, AnnotationType(test_case['data']['type']))
                else:
                    self.assertEqual(getattr(annotation, field), test_case['data'].get(field))
            
            # Check fields that should be None
            for field in test_case['expected_none']:
                self.assertIsNone(getattr(annotation, field))

    def test_probability_range(self):
        """Test annotations with different probability values"""
        test_probabilities = [0.0, 0.5, 1.0]
        
        for prob in test_probabilities:
            data = {'probability': prob}
            annotation = Annotation.from_dict(data)
            self.assertEqual(annotation.probability, prob)

    def test_position_indices(self):
        """Test annotations with different start and end positions"""
        test_positions = [
            (0, 5),    # Start of text
            (10, 20),  # Middle of text
            (95, 100)  # End of text
        ]
        
        for start, end in test_positions:
            data = {'start': start, 'end': end}
            annotation = Annotation.from_dict(data)
            self.assertEqual(annotation.start, start)
            self.assertEqual(annotation.end, end)

if __name__ == '__main__':
    unittest.main() 