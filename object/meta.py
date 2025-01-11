from dataclasses import dataclass
from typing import Optional

@dataclass
class Meta:
    result_count: Optional[int] = None
    oldest_id: Optional[str] = None
    newest_id: Optional[str] = None
    next_token: Optional[str] = None
    previous_token: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Meta':
        """
        Creates a Meta object from a dictionary
        
        Args:
            data: Dictionary containing meta information from Twitter API response
            
        Returns:
            Meta object with pagination and result metadata
        """
        if not data:
            return cls()
            
        return cls(
            result_count=data.get('result_count'),
            oldest_id=data.get('oldest_id'),
            newest_id=data.get('newest_id'),
            next_token=data.get('next_token'),
            previous_token=data.get('previous_token')
        )
