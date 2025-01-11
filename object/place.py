from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class GeoProperties:
    pass  # Twitter API returns empty properties object for places

@dataclass
class Geo:
    type: str
    bbox: List[float]
    properties: GeoProperties

@dataclass
class Place:
    id: str
    name: str
    country_code: str
    country: str
    place_type: str
    full_name: str
    geo: Geo

    @classmethod
    def from_dict(cls, data: dict) -> 'Place':
        # Convert geo data
        geo_data = data['geo']
        geo = Geo(
            type=geo_data['type'],
            bbox=geo_data['bbox'],
            properties=GeoProperties()
        )
        
        return cls(
            id=data['id'],
            name=data['name'],
            country_code=data['country_code'],
            country=data['country'],
            place_type=data['place_type'],
            full_name=data['full_name'],
            geo=geo
        )

    @classmethod
    def from_api_response(cls, response: Dict) -> Dict[str, List]:
        """
        Creates Place objects from a full API response
        
        Returns:
            Dict with 'data' and 'includes' keys containing lists of objects
        """
        result = {'data': [], 'includes': {'places': []}}
        
        # Process places in includes
        if 'includes' in response and 'places' in response['includes']:
            result['includes']['places'] = [
                cls.from_dict(place_data) 
                for place_data in response['includes']['places']
            ]
            
        return result
