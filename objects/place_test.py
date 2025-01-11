import unittest
from place import Place, PlaceType, GeoJSON, GeoBox

class TestPlace(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.place_data = {
            'id': '01a9a39529b27f36',
            'full_name': 'Manhattan, NY',
            'name': 'Manhattan',
            'place_type': 'city',
            'country': 'United States',
            'country_code': 'US',
            'contained_within': ['01a9a39529b27f37'],  # NYC's ID
            'geo': {
                'type': 'Feature',
                'bbox': [
                    -74.026675,
                    40.683935,
                    -73.910408,
                    40.877483
                ],
                'properties': {}
            }
        }
        
        self.place = Place.from_dict(self.place_data)

    def test_basic_attributes(self):
        """Test basic Place attributes"""
        self.assertEqual(self.place.id, '01a9a39529b27f36')
        self.assertEqual(self.place.full_name, 'Manhattan, NY')
        self.assertEqual(self.place.name, 'Manhattan')
        self.assertEqual(self.place.place_type, PlaceType.CITY)
        self.assertEqual(self.place.country, 'United States')
        self.assertEqual(self.place.country_code, 'US')

    def test_contained_within(self):
        """Test contained_within array"""
        self.assertEqual(self.place.contained_within, ['01a9a39529b27f37'])

    def test_geo_data(self):
        """Test GeoJSON data"""
        self.assertIsInstance(self.place.geo, GeoJSON)
        self.assertEqual(self.place.geo.type, 'Feature')
        
        # Test bounding box
        bbox = self.place.geo.bbox
        self.assertIsInstance(bbox, GeoBox)
        self.assertEqual(bbox.min_longitude, -74.026675)
        self.assertEqual(bbox.min_latitude, 40.683935)
        self.assertEqual(bbox.max_longitude, -73.910408)
        self.assertEqual(bbox.max_latitude, 40.877483)
        
        # Test properties
        self.assertEqual(self.place.geo.properties, {})

    def test_place_types(self):
        """Test different place types"""
        # Test city
        self.assertEqual(self.place.place_type, PlaceType.CITY)
        
        # Test country
        country_data = {
            **self.place_data,
            'place_type': 'country',
            'name': 'United States',
            'full_name': 'United States'
        }
        country = Place.from_dict(country_data)
        self.assertEqual(country.place_type, PlaceType.COUNTRY)
        
        # Test POI
        poi_data = {
            **self.place_data,
            'place_type': 'poi',
            'name': 'Central Park',
            'full_name': 'Central Park, Manhattan'
        }
        poi = Place.from_dict(poi_data)
        self.assertEqual(poi.place_type, PlaceType.POI)
        
        # Test neighborhood
        neighborhood_data = {
            **self.place_data,
            'place_type': 'neighborhood',
            'name': 'Upper East Side',
            'full_name': 'Upper East Side, Manhattan'
        }
        neighborhood = Place.from_dict(neighborhood_data)
        self.assertEqual(neighborhood.place_type, PlaceType.NEIGHBORHOOD)

    def test_minimal_place(self):
        """Test place creation with minimal required data"""
        minimal_data = {
            'id': '01a9a39529b27f36',
            'full_name': 'Manhattan, NY',
            'name': 'Manhattan',
            'place_type': 'city',
            'country': 'United States',
            'country_code': 'US'
        }
        
        minimal_place = Place.from_dict(minimal_data)
        
        # Test required fields
        self.assertEqual(minimal_place.id, '01a9a39529b27f36')
        self.assertEqual(minimal_place.full_name, 'Manhattan, NY')
        self.assertEqual(minimal_place.name, 'Manhattan')
        self.assertEqual(minimal_place.place_type, PlaceType.CITY)
        self.assertEqual(minimal_place.country, 'United States')
        self.assertEqual(minimal_place.country_code, 'US')
        
        # Test that optional fields are None
        self.assertIsNone(minimal_place.contained_within)
        self.assertIsNone(minimal_place.geo)

if __name__ == '__main__':
    unittest.main() 