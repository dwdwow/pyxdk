from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime

@dataclass
class Entity:
    start: int
    end: int
    url: Optional[str] = None
    expanded_url: Optional[str] = None
    display_url: Optional[str] = None
    media_key: Optional[str] = None
    probability: Optional[float] = None
    type: Optional[str] = None
    normalized_text: Optional[str] = None
    status: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    unwound_url: Optional[str] = None

@dataclass
class PublicMetrics:
    retweet_count: int
    reply_count: int
    like_count: int
    quote_count: int

@dataclass
class Domain:
    id: str
    name: str
    description: str

@dataclass
class EntityAnnotation:
    id: str
    name: str
    description: Optional[str] = None

@dataclass
class ContextAnnotation:
    domain: Domain
    entity: EntityAnnotation

@dataclass
class ReferencedTweet:
    type: str
    id: str

@dataclass
class Tweet:
    id: str
    text: str
    author_id: str
    created_at: datetime
    lang: str
    edit_history_tweet_ids: List[str]
    possibly_sensitive: bool
    public_metrics: PublicMetrics
    entities: Dict[str, List[Entity]]
    context_annotations: Optional[List[ContextAnnotation]] = None
    referenced_tweets: Optional[List[ReferencedTweet]] = None
    in_reply_to_user_id: Optional[str] = None
    attachments: Optional[Dict[str, List[str]]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Tweet':
        # Convert string datetime to datetime object
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        # Convert public metrics
        public_metrics = PublicMetrics(**data['public_metrics'])
        
        # Convert entities
        entities = {}
        if 'entities' in data:
            for key, value in data['entities'].items():
                entities[key] = [Entity(**entity) for entity in value]
        
        # Convert context annotations
        context_annotations = None
        if 'context_annotations' in data:
            context_annotations = []
            for annotation in data['context_annotations']:
                domain = Domain(**annotation['domain'])
                entity = EntityAnnotation(**annotation['entity'])
                context_annotations.append(ContextAnnotation(domain=domain, entity=entity))
        
        # Convert referenced tweets
        referenced_tweets = None
        if 'referenced_tweets' in data:
            referenced_tweets = [ReferencedTweet(**tweet) for tweet in data['referenced_tweets']]
        
        return cls(
            id=data['id'],
            text=data['text'],
            author_id=data['author_id'],
            created_at=created_at,
            lang=data['lang'],
            edit_history_tweet_ids=data['edit_history_tweet_ids'],
            possibly_sensitive=data['possibly_sensitive'],
            public_metrics=public_metrics,
            entities=entities,
            context_annotations=context_annotations,
            referenced_tweets=referenced_tweets,
            in_reply_to_user_id=data.get('in_reply_to_user_id'),
            attachments=data.get('attachments')
        )

    @classmethod
    def from_api_response(cls, response: Dict[str, Any]) -> Dict[str, List['Tweet']]:
        """
        Creates Tweet objects from a full API response including main tweets and included tweets
        
        Returns:
            Dict with 'data' and 'includes' keys containing lists of Tweet objects
        """
        result = {'data': [], 'includes': {'tweets': []}}
        
        # Process main tweets
        if 'data' in response:
            tweets_data = response['data']
            if not isinstance(tweets_data, list):
                tweets_data = [tweets_data]
            result['data'] = [cls.from_dict(tweet_data) for tweet_data in tweets_data]
        
        # Process included tweets
        if 'includes' in response and 'tweets' in response['includes']:
            result['includes']['tweets'] = [
                cls.from_dict(tweet_data) 
                for tweet_data in response['includes']['tweets']
            ]
            
        return result
