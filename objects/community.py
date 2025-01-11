from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class CommunityAccess(Enum):
    PUBLIC = "Public"
    CLOSED = "Closed"

class CommunityJoinPolicy(Enum):
    OPEN = "Open"
    RESTRICTED_JOIN_REQUESTS_DISABLED = "RestrictedJoinRequestsDisabled"
    RESTRICTED_JOIN_REQUESTS_REQUIRE_ADMIN_APPROVAL = "RestrictedJoinRequestsRequireAdminApproval"
    RESTRICTED_JOIN_REQUESTS_REQUIRE_MODERATOR_APPROVAL = "RestrictedJoinRequestsRequireModeratorApproval"
    SUPER_FOLLOW_REQUIRED = "SuperFollowRequired"

@dataclass
class Community:
    # Required fields
    id: str
    name: str
    created_at: datetime
    access: CommunityAccess
    join_policy: CommunityJoinPolicy
    member_count: int
    
    # Optional fields
    description: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Community':
        # Convert datetime string
        created_at = datetime.strptime(
            data['created_at'],
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        
        # Convert access string to enum
        access = CommunityAccess(data['access'])
        
        # Convert join_policy string to enum
        join_policy = CommunityJoinPolicy(data['join_policy'])
        
        return cls(
            id=data['id'],
            name=data['name'],
            created_at=created_at,
            access=access,
            join_policy=join_policy,
            member_count=data['member_count'],
            description=data.get('description')
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
