import unittest
from datetime import datetime
from media import Media, MediaMetrics

class TestMedia(unittest.TestCase):
    def setUp(self):
        self.sample_media_data = {
            "duration_ms": 46947,
            "type": "video",
            "height": 1080,
            "media_key": "13_1263145212760805376",
            "public_metrics": {
                "view_count": 6909260
            },
            "preview_image_url": "https://pbs.twimg.com/media/EYeX7akWsAIP1_1.jpg",
            "width": 1920
        }

        self.sample_api_response = {
            "data": [{
                "text": "Testing, testing...",
                "id": "1263145271946551300",
                "attachments": {
                    "media_keys": ["13_1263145212760805376"]
                }
            }],
            "includes": {
                "media": [self.sample_media_data]
            }
        }

    def test_media_from_dict(self):
        media = Media.from_dict(self.sample_media_data)
        
        # Test basic attributes
        self.assertEqual(media.media_key, "13_1263145212760805376")
        self.assertEqual(media.type, "video")
        self.assertEqual(media.height, 1080)
        self.assertEqual(media.width, 1920)
        self.assertEqual(media.duration_ms, 46947)
        self.assertEqual(
            media.preview_image_url,
            "https://pbs.twimg.com/media/EYeX7akWsAIP1_1.jpg"
        )
        
        # Test public metrics
        self.assertIsInstance(media.public_metrics, MediaMetrics)
        self.assertEqual(media.public_metrics.view_count, 6909260)

    # def test_media_from_api_response(self):
    #     result = Media.from_api_response(self.sample_api_response)
        
    #     # Test structure
    #     self.assertIn('includes', result)
    #     self.assertIn('media', result['includes'])
        
    #     # Test media objects
    #     self.assertEqual(len(result['includes']['media']), 1)
    #     media = result['includes']['media'][0]
    #     self.assertIsInstance(media, Media)
    #     self.assertEqual(media.media_key, "13_1263145212760805376")
    #     self.assertEqual(media.type, "video")

if __name__ == '__main__':
    unittest.main() 