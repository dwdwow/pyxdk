from dataclasses import dataclass
from typing import Dict, List as TypeList, Optional
from datetime import datetime
from user import User

@dataclass
class List:
    id: str
    name: str
    member_count: int
    follower_count: int
    owner_id: str
    created_at: datetime
    private: bool
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'List':
        # Convert string datetime to datetime object
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        return cls(
            id=data['id'],
            name=data['name'],
            member_count=data['member_count'],
            follower_count=data['follower_count'],
            owner_id=data['owner_id'],
            created_at=created_at,
            private=data['private'],
            description=data.get('description')
        )

    @classmethod
    def from_api_response(cls, response: Dict) -> Dict[str, TypeList]:
        """
        Creates List objects from a full API response including lists and included users
        
        Returns:
            Dict with 'data' and 'includes' keys containing List and User objects
        """
        result = {'data': None, 'includes': {'users': []}}
        
        # Process list data
        if 'data' in response:
            list_data = response['data']
            result['data'] = cls.from_dict(list_data)
        
        # Process included users
        if 'includes' in response and 'users' in response['includes']:
            result['includes']['users'] = [
                User.from_dict(user_data) 
                for user_data in response['includes']['users']
            ]
            
        return result
