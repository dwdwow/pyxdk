from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class MediaMetrics:
    view_count: int

@dataclass
class Media:
    media_key: str
    type: str
    height: int
    width: int
    preview_image_url: Optional[str] = None
    duration_ms: Optional[int] = None
    public_metrics: Optional[MediaMetrics] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Media':
        # Convert public metrics if present
        public_metrics = None
        if 'public_metrics' in data:
            public_metrics = MediaMetrics(**data['public_metrics'])
        
        return cls(
            media_key=data['media_key'],
            type=data['type'],
            height=data['height'],
            width=data['width'],
            preview_image_url=data.get('preview_image_url'),
            duration_ms=data.get('duration_ms'),
            public_metrics=public_metrics
        )

    @classmethod
    def from_api_response(cls, response: Dict) -> Dict[str, List]:
        """
        Creates Media objects from a full API response
        
        Returns:
            Dict with 'data' and 'includes' keys containing lists of objects
        """
        result = {'data': [], 'includes': {'media': []}}
        
        # Process media in includes
        if 'includes' in response and 'media' in response['includes']:
            result['includes']['media'] = [
                cls.from_dict(media_data) 
                for media_data in response['includes']['media']
            ]
            
        return result
