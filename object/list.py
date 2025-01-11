from dataclasses import dataclass
from typing import Dict, List as TypeList, Optional
from datetime import datetime
from user import User

@dataclass
class List:
    # Required fields
    id: str
    name: str
    owner_id: str
    private: bool
    follower_count: int
    member_count: int
    
    # Optional fields
    created_at: datetime | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'List':
        # Convert datetime string to datetime object
        created_at = None
        if 'created_at' in data and data['created_at']:
            created_at = datetime.strptime(
                data['created_at'],
                '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        
        return cls(
            id=data['id'],
            name=data['name'],
            owner_id=data['owner_id'],
            private=data['private'],
            follower_count=data['follower_count'],
            member_count=data['member_count'],
            created_at=created_at,
            description=data.get('description')
        )
