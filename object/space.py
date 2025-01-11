from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from user import User

@dataclass
class Space:
    id: str
    state: str
    created_at: datetime
    host_ids: List[str]
    lang: str
    is_ticketed: bool
    title: str
    updated_at: datetime
    invited_user_ids: Optional[List[str]] = None
    participant_count: Optional[int] = None
    scheduled_start: Optional[datetime] = None
    speaker_ids: Optional[List[str]] = None
    started_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Space':
        # Convert datetime strings to datetime objects
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        updated_at = datetime.strptime(data['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        # Handle optional datetime fields
        scheduled_start = None
        if 'scheduled_start' in data:
            scheduled_start = datetime.strptime(data['scheduled_start'], '%Y-%m-%dT%H:%M:%S.%fZ')
            
        started_at = None
        if 'started_at' in data:
            started_at = datetime.strptime(data['started_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        return cls(
            id=data['id'],
            state=data['state'],
            created_at=created_at,
            host_ids=data['host_ids'],
            lang=data['lang'],
            is_ticketed=data['is_ticketed'],
            title=data['title'],
            updated_at=updated_at,
            invited_user_ids=data.get('invited_user_ids'),
            participant_count=data.get('participant_count'),
            scheduled_start=scheduled_start,
            speaker_ids=data.get('speaker_ids'),
            started_at=started_at
        )

    @classmethod
    def from_api_response(cls, response: Dict) -> Dict[str, List]:
        """
        Creates Space objects from a full API response including spaces and included users
        
        Returns:
            Dict with 'data' and 'includes' keys containing Space and User objects
        """
        result = {'data': None, 'includes': {'users': []}}
        
        # Process space data
        if 'data' in response:
            space_data = response['data']
            result['data'] = cls.from_dict(space_data)
        
        # Process included users
        if 'includes' in response and 'users' in response['includes']:
            result['includes']['users'] = [
                User.from_dict(user_data) 
                for user_data in response['includes']['users']
            ]
            
        return result
