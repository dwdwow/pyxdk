from dataclasses import dataclass
from enum import Enum

class AnnotationType(Enum):
    PERSON = "Person"
    PLACE = "Place"
    PRODUCT = "Product"
    ORGANIZATION = "Organization"
    OTHER = "Other"

@dataclass
class Annotation:
    # All fields are optional
    start: int | None = None
    end: int | None = None  # Note: Currently inclusive, will be exclusive in v3
    probability: float | None = None
    annotation_type: AnnotationType | None = None
    normalized_text: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Annotation':
        # Convert type string to enum if present
        annotation_type = None
        if 'type' in data:
            annotation_type = AnnotationType(data['type'])
        
        return cls(
            start=data.get('start'),
            end=data.get('end'),
            probability=data.get('probability'),
            annotation_type=annotation_type,
            normalized_text=data.get('normalized_text')
        )
