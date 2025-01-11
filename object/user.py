from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from tweet import Tweet

@dataclass
class UrlEntity:
    start: int
    end: int
    url: str
    expanded_url: str
    display_url: str

@dataclass
class HashtagEntity:
    start: int
    end: int
    tag: str

@dataclass
class UserEntities:
    url: Optional[Dict[str, List[UrlEntity]]] = None
    description: Optional[Dict[str, List[HashtagEntity]]] = None

@dataclass
class User:
    id: str
    name: str
    username: str
    created_at: datetime
    verified: bool
    description: str
    protected: bool
    entities: UserEntities
    url: Optional[str] = None
    location: Optional[str] = None
    profile_image_url: Optional[str] = None
    pinned_tweet_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        # Convert string datetime to datetime object
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        # Convert entities
        entities = {}
        if 'entities' in data:
            # Handle URL entities
            if 'url' in data['entities']:
                url_entities = [
                    UrlEntity(**url_data)
                    for url_data in data['entities']['url']['urls']
                ]
                entities['url'] = {'urls': url_entities}
            
            # Handle description entities (hashtags)
            if 'description' in data['entities']:
                hashtag_entities = [
                    HashtagEntity(**hashtag_data)
                    for hashtag_data in data['entities']['description']['hashtags']
                ]
                entities['description'] = {'hashtags': hashtag_entities}
        
        user_entities = UserEntities(**entities)
        
        return cls(
            id=data['id'],
            name=data['name'],
            username=data['username'],
            created_at=created_at,
            verified=data['verified'],
            description=data['description'],
            protected=data['protected'],
            entities=user_entities,
            url=data.get('url'),
            location=data.get('location'),
            profile_image_url=data.get('profile_image_url'),
            pinned_tweet_id=data.get('pinned_tweet_id')
        )

    # @classmethod
    # def from_api_response(cls, response: Dict) -> Dict[str, List]:
    #     """
    #     Creates User objects from a full API response including users and included tweets
        
    #     Returns:
    #         Dict with 'data' and 'includes' keys containing lists of User and Tweet objects
    #     """
    #     result = {'data': [], 'includes': {'tweets': []}}
        
    #     # Process users
    #     if 'data' in response:
    #         users_data = response['data']
    #         if not isinstance(users_data, list):
    #             users_data = [users_data]
    #         result['data'] = [cls.from_dict(user_data) for user_data in users_data]
        
    #     # Process included tweets
    #     if 'includes' in response and 'tweets' in response['includes']:
    #         result['includes']['tweets'] = [
    #             Tweet.from_dict(tweet_data) 
    #             for tweet_data in response['includes']['tweets']
    #         ]
            
        return result
