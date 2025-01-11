from dataclasses import dataclass
from enum import Enum

class PlaceType(Enum):
    CITY = "city"
    COUNTRY = "country"
    ADMIN = "admin"
    POI = "poi"  # Point of Interest
    NEIGHBORHOOD = "neighborhood"

@dataclass
class GeoBox:
    min_longitude: float
    min_latitude: float
    max_longitude: float
    max_latitude: float

    @classmethod
    def from_bbox(cls, bbox: list[float]) -> 'GeoBox':
        return cls(
            min_longitude=bbox[0],
            min_latitude=bbox[1],
            max_longitude=bbox[2],
            max_latitude=bbox[3]
        )

@dataclass
class GeoJSON:
    type: str
    bbox: GeoBox
    properties: dict

    @classmethod
    def from_dict(cls, data: dict) -> 'GeoJSON':
        return cls(
            type=data['type'],
            bbox=GeoBox.from_bbox(data['bbox']),
            properties=data.get('properties', {})
        )

@dataclass
class Place:
    # Required fields
    id: str
    full_name: str
    name: str
    place_type: PlaceType
    country: str
    country_code: str
    
    # Optional fields
    contained_within: list[str] | None = None
    geo: GeoJSON | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Place':
        # Convert place_type string to enum
        place_type = PlaceType(data['place_type'])
        
        # Convert geo data if present
        geo = None
        if 'geo' in data and data['geo']:
            geo = GeoJSON.from_dict(data['geo'])
        
        return cls(
            id=data['id'],
            full_name=data['full_name'],
            name=data['name'],
            place_type=place_type,
            country=data['country'],
            country_code=data['country_code'],
            contained_within=data.get('contained_within'),
            geo=geo
        )
