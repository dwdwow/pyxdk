from dataclasses import dataclass
from datetime import datetime

from object.annotation import Annotation

@dataclass
class PublicMetrics:
    retweet_count: int
    reply_count: int
    like_count: int
    quote_count: int

@dataclass
class NonPublicMetrics:
    impression_count: int
    url_link_clicks: int
    user_profile_clicks: int

@dataclass
class OrganicMetrics:
    impression_count: int
    like_count: int
    reply_count: int
    retweet_count: int
    url_link_clicks: int
    user_profile_clicks: int

@dataclass
class PromotedMetrics:
    impression_count: int
    like_count: int
    reply_count: int
    retweet_count: int
    url_link_clicks: int
    user_profile_clicks: int

@dataclass
class Domain:
    id: str
    name: str
    description: str

@dataclass
class EntityAnnotation:
    id: str
    name: str
    description: str | None = None

@dataclass
class ContextAnnotation:
    domain: Domain
    entity: EntityAnnotation

@dataclass
class ReferencedTweet:
    reference_type: str
    id: str

@dataclass
class EditControls:
    edits_remaining: int
    is_edit_eligible: bool
    editable_until: datetime

@dataclass
class Withheld:
    copyright: bool
    country_codes: list[str]

@dataclass
class Cashtag:
    start: int
    end: int  # Exclusive
    tag: str

@dataclass
class Hashtag:
    start: int
    end: int  # Exclusive
    tag: str

@dataclass
class Mention:
    start: int
    end: int  # Exclusive
    tag: str

@dataclass
class Url:
    start: int
    end: int  # Exclusive
    url: str
    expanded_url: str
    display_url: str
    status: str | None = None
    title: str | None = None
    description: str | None = None
    unwound_url: str | None = None

@dataclass
class Entities:
    # All fields are optional as tweets may not have all types of entities
    annotations: list[Annotation] | None = None
    cashtags: list[Cashtag] | None = None
    hashtags: list[Hashtag] | None = None
    mentions: list[Mention] | None = None
    urls: list[Url] | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Entities':
        # Convert annotations if present
        annotations = None
        if 'annotations' in data:
            annotations = [
                Annotation(
                    start=ann['start'],
                    end=ann['end'],
                    probability=ann['probability'],
                    type=ann['type'],
                    normalized_text=ann['normalized_text']
                )
                for ann in data['annotations']
            ]
        
        # Convert cashtags if present
        cashtags = None
        if 'cashtags' in data:
            cashtags = [
                Cashtag(
                    start=tag['start'],
                    end=tag['end'],
                    tag=tag['tag']
                )
                for tag in data['cashtags']
            ]
        
        # Convert hashtags if present
        hashtags = None
        if 'hashtags' in data:
            hashtags = [
                Hashtag(
                    start=tag['start'],
                    end=tag['end'],
                    tag=tag['tag']
                )
                for tag in data['hashtags']
            ]
        
        # Convert mentions if present
        mentions = None
        if 'mentions' in data:
            mentions = [
                Mention(
                    start=mention['start'],
                    end=mention['end'],
                    tag=mention['tag']
                )
                for mention in data['mentions']
            ]
        
        # Convert urls if present
        urls = None
        if 'urls' in data:
            urls = [
                Url(
                    start=url['start'],
                    end=url['end'],
                    url=url['url'],
                    expanded_url=url['expanded_url'],
                    display_url=url['display_url'],
                    status=url.get('status'),
                    title=url.get('title'),
                    description=url.get('description'),
                    unwound_url=url.get('unwound_url')
                )
                for url in data['urls']
            ]
        
        return cls(
            annotations=annotations,
            cashtags=cashtags,
            hashtags=hashtags,
            mentions=mentions,
            urls=urls
        )

@dataclass
class Tweet:
    # Required fields
    id: str
    text: str
    author_id: str
    created_at: datetime
    edit_history_tweet_ids: list[str]
    
    # Optional fields
    lang: str | None = None
    possibly_sensitive: bool | None = None
    public_metrics: PublicMetrics | None = None
    entities: Entities | None = None
    context_annotations: list[ContextAnnotation] | None = None
    referenced_tweets: list[ReferencedTweet] | None = None
    in_reply_to_user_id: str | None = None
    attachments: dict[str, list[str]] | None = None
    conversation_id: str | None = None
    edit_controls: EditControls | None = None
    non_public_metrics: NonPublicMetrics | None = None
    organic_metrics: OrganicMetrics | None = None
    promoted_metrics: PromotedMetrics | None = None
    reply_settings: str | None = None
    withheld: Withheld | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Tweet':
        # Convert datetime strings
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        # Convert metrics
        public_metrics = PublicMetrics(**data['public_metrics'])
        
        # Convert entities if present
        entities = None
        if 'entities' in data:
            entities = Entities.from_dict(data['entities'])
        
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
            referenced_tweets = []
            for tweet in data['referenced_tweets']:
                # Rename 'type' to 'reference_type' in referenced tweet data
                tweet_data = tweet.copy()
                tweet_data['reference_type'] = tweet_data.pop('type')
                referenced_tweets.append(ReferencedTweet(**tweet_data))
        
        # Convert edit controls
        edit_controls = None
        if 'edit_controls' in data:
            edit_data = data['edit_controls']
            edit_data['editable_until'] = datetime.strptime(
                edit_data['editable_until'], 
                '%Y-%m-%dT%H:%M:%S.%fZ'
            )
            edit_controls = EditControls(**edit_data)
        
        # Convert metrics if present
        non_public_metrics = None
        if 'non_public_metrics' in data:
            non_public_metrics = NonPublicMetrics(**data['non_public_metrics'])
            
        organic_metrics = None
        if 'organic_metrics' in data:
            organic_metrics = OrganicMetrics(**data['organic_metrics'])
            
        promoted_metrics = None
        if 'promoted_metrics' in data:
            promoted_metrics = PromotedMetrics(**data['promoted_metrics'])
            
        # Convert withheld
        withheld = None
        if 'withheld' in data:
            withheld = Withheld(**data['withheld'])
        
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
            attachments=data.get('attachments'),
            conversation_id=data.get('conversation_id'),
            edit_controls=edit_controls,
            non_public_metrics=non_public_metrics,
            organic_metrics=organic_metrics,
            promoted_metrics=promoted_metrics,
            reply_settings=data.get('reply_settings'),
            withheld=withheld
        )
