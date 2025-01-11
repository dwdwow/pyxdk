from dataclasses import dataclass
from enum import Enum

class MediaType(Enum):
    ANIMATED_GIF = "animated_gif"
    PHOTO = "photo"
    VIDEO = "video"

@dataclass
class MediaVariant:
    content_type: str
    url: str
    bit_rate: int | None = None

@dataclass
class MediaMetrics:
    playback_0_count: int
    playback_25_count: int
    playback_50_count: int
    playback_75_count: int
    playback_100_count: int
    view_count: int | None = None

@dataclass
class Media:
    # Required fields
    media_key: str
    type: MediaType
    height: int
    width: int
    
    # Optional fields
    url: str | None = None
    duration_ms: int | None = None
    preview_image_url: str | None = None
    alt_text: str | None = None
    
    # Metrics
    non_public_metrics: MediaMetrics | None = None
    organic_metrics: MediaMetrics | None = None
    promoted_metrics: MediaMetrics | None = None
    public_metrics: dict[str, int] | None = None
    
    # Variants
    variants: list[MediaVariant] | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Media':
        # Convert type string to enum
        media_type = MediaType(data['type'])
        
        # Convert metrics if present
        metrics_fields = ['non_public_metrics', 'organic_metrics', 'promoted_metrics']
        metrics = {}
        
        for field in metrics_fields:
            if field in data:
                metrics[field] = MediaMetrics(
                    playback_0_count=data[field]['playback_0_count'],
                    playback_25_count=data[field]['playback_25_count'],
                    playback_50_count=data[field]['playback_50_count'],
                    playback_75_count=data[field]['playback_75_count'],
                    playback_100_count=data[field]['playback_100_count'],
                    view_count=data[field].get('view_count')
                )
            else:
                metrics[field] = None
        
        # Convert variants if present
        variants = None
        if 'variants' in data:
            variants = [
                MediaVariant(
                    content_type=variant['content_type'],
                    url=variant['url'],
                    bit_rate=variant.get('bit_rate')
                )
                for variant in data['variants']
            ]
        
        return cls(
            media_key=data['media_key'],
            type=media_type,
            height=data['height'],
            width=data['width'],
            url=data.get('url'),
            duration_ms=data.get('duration_ms'),
            preview_image_url=data.get('preview_image_url'),
            alt_text=data.get('alt_text'),
            non_public_metrics=metrics['non_public_metrics'],
            organic_metrics=metrics['organic_metrics'],
            promoted_metrics=metrics['promoted_metrics'],
            public_metrics=data.get('public_metrics'),
            variants=variants
        )
