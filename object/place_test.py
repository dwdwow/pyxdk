import unittest
from place import Place, Geo, GeoProperties

class TestPlace(unittest.TestCase):
    def setUp(self):
        self.sample_place_data = {
            "geo": {
                "type": "Feature",
                "bbox": [
                    -74.026675,
                    40.683935,
                    -73.910408,
                    40.877483
                ],
                "properties": {}
            },
            "country_code": "US",
            "name": "Manhattan",
            "id": "01a9a39529b27f36",
            "place_type": "city",
            "country": "United States",
            "full_name": "Manhattan, NY"
        }

        self.sample_api_response = {
            "data": [{
                "text": "We're sharing a live demo...",
                "id": "1136048014974423040",
                "geo": {
                    "place_id": "01a9a39529b27f36"
                }
            }],
            "includes": {
                "places": [self.sample_place_data]
            }
        }

    def test_place_from_dict(self):
        place = Place.from_dict(self.sample_place_data)
        
        # Test basic attributes
        self.assertEqual(place.id, "01a9a39529b27f36")
        self.assertEqual(place.name, "Manhattan")
        self.assertEqual(place.country_code, "US")
        self.assertEqual(place.country, "United States")
        self.assertEqual(place.place_type, "city")
        self.assertEqual(place.full_name, "Manhattan, NY")
        
        # Test geo data
        self.assertIsInstance(place.geo, Geo)
        self.assertEqual(place.geo.type, "Feature")
        self.assertEqual(len(place.geo.bbox), 4)
        self.assertEqual(place.geo.bbox[0], -74.026675)
        self.assertEqual(place.geo.bbox[1], 40.683935)
        self.assertIsInstance(place.geo.properties, GeoProperties)

    def test_place_from_api_response(self):
        result = Place.from_api_response(self.sample_api_response)
        
        # Test structure
        self.assertIn('includes', result)
        self.assertIn('places', result['includes'])
        
        # Test places
        self.assertEqual(len(result['includes']['places']), 1)
        place = result['includes']['places'][0]
        self.assertIsInstance(place, Place)
        self.assertEqual(place.id, "01a9a39529b27f36")
        self.assertEqual(place.name, "Manhattan")

if __name__ == '__main__':
    unittest.main() 