from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class SpaceState(Enum):
    LIVE = "live"
    SCHEDULED = "scheduled"
    ENDED = "ended"

@dataclass
class Space:
    # Required fields
    id: str
    state: SpaceState
    title: str
    host_ids: list[str]
    participant_count: int
    
    # Optional fields with timestamps
    created_at: datetime | None = None
    ended_at: datetime | None = None
    started_at: datetime | None = None
    scheduled_start: datetime | None = None
    updated_at: datetime | None = None
    
    # Optional fields with arrays
    invited_user_ids: list[str] | None = None
    speaker_ids: list[str] | None = None
    topic_ids: list[str] | None = None
    
    # Optional scalar fields
    lang: str | None = None
    is_ticketed: bool = False
    subscriber_count: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Space':
        # Convert datetime strings to datetime objects
        datetime_fields = {
            'created_at': None,
            'ended_at': None,
            'started_at': None,
            'scheduled_start': None,
            'updated_at': None
        }
        
        for field in datetime_fields:
            if field in data and data[field]:
                datetime_fields[field] = datetime.strptime(
                    data[field],
                    '%Y-%m-%dT%H:%M:%S.%fZ'
                )
        
        # Convert state string to enum
        state = SpaceState(data['state'])
        
        # Handle array fields with empty list defaults
        array_fields = {
            'host_ids': data.get('host_ids', []),
            'invited_user_ids': data.get('invited_user_ids'),
            'speaker_ids': data.get('speaker_ids'),
            'topic_ids': data.get('topic_ids')
        }
        
        return cls(
            # Required fields
            id=data['id'],
            state=state,
            title=data['title'],
            host_ids=array_fields['host_ids'],
            participant_count=data['participant_count'],
            
            # Optional timestamp fields
            created_at=datetime_fields['created_at'],
            ended_at=datetime_fields['ended_at'],
            started_at=datetime_fields['started_at'],
            scheduled_start=datetime_fields['scheduled_start'],
            updated_at=datetime_fields['updated_at'],
            
            # Optional array fields
            invited_user_ids=array_fields['invited_user_ids'],
            speaker_ids=array_fields['speaker_ids'],
            topic_ids=array_fields['topic_ids'],
            
            # Optional scalar fields
            lang=data.get('lang'),
            is_ticketed=data.get('is_ticketed', False),
            subscriber_count=data.get('subscriber_count')
        )
