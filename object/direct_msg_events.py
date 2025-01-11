from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class EventType(Enum):
    MESSAGE_CREATE = "MessageCreate"
    PARTICIPANTS_JOIN = "ParticipantsJoin"
    PARTICIPANTS_LEAVE = "ParticipantsLeave"

@dataclass
class ReferencedTweet:
    id: str

@dataclass
class Attachments:
    media_keys: list[str]

@dataclass
class DirectMessageEvent:
    # Required fields
    id: str
    event_type: EventType
    sender_id: str
    dm_conversation_id: str
    created_at: datetime
    
    # Optional fields
    text: str | None = None
    participant_ids: list[str] | None = None
    referenced_tweets: list[ReferencedTweet] | None = None
    attachments: Attachments | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'DirectMessageEvent':
        # Convert event_type string to enum
        event_type = EventType(data['event_type'])
        
        # Convert datetime string
        created_at = datetime.strptime(
            data['created_at'],
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        
        # Convert referenced tweets if present
        referenced_tweets = None
        if 'referenced_tweets' in data:
            referenced_tweets = [
                ReferencedTweet(id=tweet['id'])
                for tweet in data['referenced_tweets']
            ]
        
        # Convert attachments if present
        attachments = None
        if 'attachments' in data:
            attachments = Attachments(
                media_keys=data['attachments']['media_keys']
            )
        
        return cls(
            id=data['id'],
            event_type=event_type,
            sender_id=data['sender_id'],
            dm_conversation_id=data['dm_conversation_id'],
            created_at=created_at,
            text=data.get('text'),
            participant_ids=data.get('participant_ids'),
            referenced_tweets=referenced_tweets,
            attachments=attachments
        ) 