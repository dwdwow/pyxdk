from dataclasses import dataclass
from datetime import datetime

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
class MentionEntity:
    start: int
    end: int
    tag: str

@dataclass
class CashtagEntity:
    start: int
    end: int
    tag: str

@dataclass
class UserEntities:
    url: dict[str, list[UrlEntity]] | None = None
    description: dict[str, list[UrlEntity | HashtagEntity | MentionEntity | CashtagEntity]] | None = None

@dataclass
class UserPublicMetrics:
    followers_count: int
    following_count: int
    tweet_count: int
    listed_count: int

@dataclass
class Withheld:
    country_codes: list[str]
    scope: str | None = None

@dataclass
class User:
    # Required fields
    id: str
    name: str
    username: str
    created_at: datetime
    description: str
    protected: bool
    verified: bool
    entities: UserEntities
    public_metrics: UserPublicMetrics
    
    # Optional fields
    url: str | None = None
    location: str | None = None
    pinned_tweet_id: str | None = None
    profile_image_url: str | None = None
    connection_status: list[str] | None = None
    withheld: Withheld | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        # Convert datetime string
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
            
            # Handle description entities
            if 'description' in data['entities']:
                desc_entities = {}
                
                # Handle URLs in description
                if 'urls' in data['entities']['description']:
                    desc_entities['urls'] = [
                        UrlEntity(**url_data)
                        for url_data in data['entities']['description']['urls']
                    ]
                
                # Handle hashtags in description
                if 'hashtags' in data['entities']['description']:
                    desc_entities['hashtags'] = [
                        HashtagEntity(**hashtag_data)
                        for hashtag_data in data['entities']['description']['hashtags']
                    ]
                
                # Handle mentions in description
                if 'mentions' in data['entities']['description']:
                    desc_entities['mentions'] = [
                        MentionEntity(**mention_data)
                        for mention_data in data['entities']['description']['mentions']
                    ]
                
                # Handle cashtags in description
                if 'cashtags' in data['entities']['description']:
                    desc_entities['cashtags'] = [
                        CashtagEntity(**cashtag_data)
                        for cashtag_data in data['entities']['description']['cashtags']
                    ]
                
                entities['description'] = desc_entities
        
        user_entities = UserEntities(**entities)
        
        # Convert public metrics
        public_metrics = UserPublicMetrics(**data['public_metrics'])
        
        # Convert withheld if present
        withheld = None
        if 'withheld' in data:
            withheld = Withheld(**data['withheld'])
        
        return cls(
            id=data['id'],
            name=data['name'],
            username=data['username'],
            created_at=created_at,
            description=data['description'],
            protected=data['protected'],
            verified=data['verified'],
            entities=user_entities,
            public_metrics=public_metrics,
            url=data.get('url'),
            location=data.get('location'),
            pinned_tweet_id=data.get('pinned_tweet_id'),
            profile_image_url=data.get('profile_image_url'),
            connection_status=data.get('connection_status'),
            withheld=withheld
        )
