from dataclasses import dataclass
from typing import Optional, TypeVar, TypedDict
from object.community import Community
from object.direct_msg_events import DirectMessageEvent
from object.list import List
from object.media import Media
from object.meta import Meta
from object.place import Place
from object.poll import Poll
from object.space import Space
from object.tweet import Tweet
from object.user import User


DataItem = TypeVar('DataItem', Tweet, User, Space, List, Media, Poll, Place, Community, DirectMessageEvent)


@dataclass
class Includes:
    tweets: list[Tweet] | None
    users: list[User] | None
    spaces: list[Space] | None
    lists: list[List] | None
    media: list[Media] | None
    polls: list[Poll] | None
    places: list[Place] | None
    communities: list[Community] | None
    direct_message_events: list[DirectMessageEvent] | None
    meta: Meta | None

    @classmethod
    def from_dict(cls, data: dict) -> 'Includes':
        return cls(**data)
    
    
RawData = TypedDict('RawData', {
    'data': list[DataItem],
    'includes': Includes
})


@dataclass
class ResponseData:
    data: list[DataItem]
    includes: Includes

    @classmethod
    def from_dict(cls, data: RawData[DataItem]) -> 'ResponseData':
        return cls(
            data=[DataItem.from_dict(item) for item in data['data']],
            includes=Includes.from_dict(data['includes'])
        )
