from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from tweet import Tweet
from user import User

@dataclass
class ReferencedTweet:
    id: str

@dataclass
class DirectMessageEvent:
    id: str
    sender_id: str
    text: str
    created_at: datetime
    event_type: str
    dm_conversation_id: str
    referenced_tweets: Optional[List[ReferencedTweet]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'DirectMessageEvent':
        # Convert string datetime to datetime object
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        # Convert referenced tweets if present
        referenced_tweets = None
        if 'referenced_tweets' in data:
            referenced_tweets = [
                ReferencedTweet(**tweet)
                for tweet in data['referenced_tweets']
            ]
        
        return cls(
            id=data['id'],
            sender_id=data['sender_id'],
            text=data['text'],
            created_at=created_at,
            event_type=data['event_type'],
            dm_conversation_id=data['dm_conversation_id'],
            referenced_tweets=referenced_tweets
        )

    # @classmethod
    # def from_api_response(cls, response: Dict) -> Dict[str, List]:
    #     """
    #     Creates DirectMessageEvent objects from a full API response including DM events and included data
        
    #     Returns:
    #         Dict with 'data', 'includes', and 'meta' keys containing lists of objects
    #     """
    #     result = {
    #         'data': [],
    #         'includes': {
    #             'users': [],
    #             'tweets': []
    #         },
    #         'meta': response.get('meta', {})
    #     }
        
    #     # Process DM events
    #     if 'data' in response:
    #         result['data'] = [
    #             cls.from_dict(event_data) 
    #             for event_data in response['data']
    #         ]
        
    #     # Process included users
    #     if 'includes' in response and 'users' in response['includes']:
    #         result['includes']['users'] = [
    #             User.from_dict(user_data) 
    #             for user_data in response['includes']['users']
    #         ]
            
    #     # Process included tweets
    #     if 'includes' in response and 'tweets' in response['includes']:
    #         result['includes']['tweets'] = [
    #             Tweet.from_dict(tweet_data) 
    #             for tweet_data in response['includes']['tweets']
    #         ]
            
        return result 