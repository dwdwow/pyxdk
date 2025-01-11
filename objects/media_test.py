import unittest
from media import Media, MediaType, MediaVariant, MediaMetrics

class TestMedia(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.media_data = {
            'media_key': '13_1263145212760805376',
            'type': 'video',
            'duration_ms': 46947,
            'height': 1080,
            'width': 1920,
            'url': 'https://video.twimg.com/media/sample.mp4',
            'preview_image_url': 'https://pbs.twimg.com/media/EYeX7akWsAIP1_1.jpg',
            'alt_text': 'Rugged hills along the Na Pali coast on the island of Kauai',
            'non_public_metrics': {
                'playback_0_count': 1561,
                'playback_100_count': 116,
                'playback_25_count': 559,
                'playback_50_count': 305,
                'playback_75_count': 183
            },
            'organic_metrics': {
                'playback_0_count': 1561,
                'playback_100_count': 116,
                'playback_25_count': 559,
                'playback_50_count': 305,
                'playback_75_count': 183,
                'view_count': 629
            },
            'promoted_metrics': {
                'playback_0_count': 259,
                'playback_100_count': 15,
                'playback_25_count': 113,
                'playback_50_count': 57,
                'playback_75_count': 25,
                'view_count': 124
            },
            'public_metrics': {
                'view_count': 6865141
            },
            'variants': [
                {
                    'bit_rate': 632000,
                    'content_type': 'video/mp4',
                    'url': 'https://video.twimg.com/ext_tw_video/1527322141724532740/pu/vid/320x568/sample.mp4'
                }
            ]
        }
        
        self.media = Media.from_dict(self.media_data)

    def test_basic_attributes(self):
        """Test basic Media attributes"""
        self.assertEqual(self.media.media_key, '13_1263145212760805376')
        self.assertEqual(self.media.type, MediaType.VIDEO)
        self.assertEqual(self.media.duration_ms, 46947)
        self.assertEqual(self.media.height, 1080)
        self.assertEqual(self.media.width, 1920)
        self.assertEqual(
            self.media.url,
            'https://video.twimg.com/media/sample.mp4'
        )
        self.assertEqual(
            self.media.preview_image_url,
            'https://pbs.twimg.com/media/EYeX7akWsAIP1_1.jpg'
        )
        self.assertEqual(
            self.media.alt_text,
            'Rugged hills along the Na Pali coast on the island of Kauai'
        )

    def test_metrics(self):
        """Test media metrics"""
        # Test non-public metrics
        self.assertIsInstance(self.media.non_public_metrics, MediaMetrics)
        self.assertEqual(self.media.non_public_metrics.playback_0_count, 1561)
        self.assertEqual(self.media.non_public_metrics.playback_100_count, 116)
        self.assertIsNone(self.media.non_public_metrics.view_count)
        
        # Test organic metrics
        self.assertIsInstance(self.media.organic_metrics, MediaMetrics)
        self.assertEqual(self.media.organic_metrics.playback_0_count, 1561)
        self.assertEqual(self.media.organic_metrics.view_count, 629)
        
        # Test promoted metrics
        self.assertIsInstance(self.media.promoted_metrics, MediaMetrics)
        self.assertEqual(self.media.promoted_metrics.playback_0_count, 259)
        self.assertEqual(self.media.promoted_metrics.view_count, 124)
        
        # Test public metrics
        self.assertEqual(self.media.public_metrics['view_count'], 6865141)

    def test_variants(self):
        """Test media variants"""
        self.assertIsInstance(self.media.variants[0], MediaVariant)
        variant = self.media.variants[0]
        self.assertEqual(variant.bit_rate, 632000)
        self.assertEqual(variant.content_type, 'video/mp4')
        self.assertEqual(
            variant.url,
            'https://video.twimg.com/ext_tw_video/1527322141724532740/pu/vid/320x568/sample.mp4'
        )

    def test_media_types(self):
        """Test different media types"""
        # Test photo
        photo_data = {
            **self.media_data,
            'type': 'photo',
            'duration_ms': None
        }
        photo = Media.from_dict(photo_data)
        self.assertEqual(photo.type, MediaType.PHOTO)
        self.assertIsNone(photo.duration_ms)
        
        # Test animated GIF
        gif_data = {
            **self.media_data,
            'type': 'animated_gif'
        }
        gif = Media.from_dict(gif_data)
        self.assertEqual(gif.type, MediaType.ANIMATED_GIF)

    def test_minimal_media(self):
        """Test media creation with minimal required data"""
        minimal_data = {
            'media_key': '13_1263145212760805376',
            'type': 'photo',
            'height': 1080,
            'width': 1920
        }
        
        minimal_media = Media.from_dict(minimal_data)
        
        # Test required fields
        self.assertEqual(minimal_media.media_key, '13_1263145212760805376')
        self.assertEqual(minimal_media.type, MediaType.PHOTO)
        self.assertEqual(minimal_media.height, 1080)
        self.assertEqual(minimal_media.width, 1920)
        
        # Test that optional fields are None
        self.assertIsNone(minimal_media.url)
        self.assertIsNone(minimal_media.duration_ms)
        self.assertIsNone(minimal_media.preview_image_url)
        self.assertIsNone(minimal_media.alt_text)
        self.assertIsNone(minimal_media.non_public_metrics)
        self.assertIsNone(minimal_media.organic_metrics)
        self.assertIsNone(minimal_media.promoted_metrics)
        self.assertIsNone(minimal_media.public_metrics)
        self.assertIsNone(minimal_media.variants)

if __name__ == '__main__':
    unittest.main() 