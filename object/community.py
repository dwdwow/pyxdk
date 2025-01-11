from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Community:
    id: str
    name: str
    description: str
    join_policy: str
    access: str
    member_count: int
    created_at: datetime

    @classmethod
    def from_dict(cls, data: dict) -> 'Community':
        # Convert string datetime to datetime object
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            join_policy=data['join_policy'],
            access=data['access'],
            member_count=data['member_count'],
            created_at=created_at
        )

    # @classmethod
    # def from_api_response(cls, response: Dict) -> Dict[str, List]:
    #     """
    #     Creates Community objects from a full API response
        
    #     Returns:
    #         Dict with 'data' and 'meta' keys containing lists of objects
    #     """
    #     result = {
    #         'data': [],
    #         'meta': response.get('meta', {})
    #     }
        
    #     # Process communities
    #     if 'data' in response:
    #         result['data'] = [
    #             cls.from_dict(community_data) 
    #             for community_data in response['data']
    #         ]
            
    #     return result
