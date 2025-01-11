from dataclasses import dataclass
from typing import TypeVar, TypedDict
from community import Community
from direct_msg_events import DirectMessageEvent
from errors import Errors
from xlist import List
from media import Media
from meta import Meta
from place import Place
from poll import Poll
from space import Space
from tweet import Tweet
from user import User


DataItem = TypeVar('DataItem', Tweet, User, Space, List, Media, Poll, Place, Community, DirectMessageEvent)
RespDataType = TypeVar('RespDataType', list[DataItem], DataItem, None)


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
    'data': RespDataType,  
    'includes': Includes | None,
    'meta': Meta | None,
    'errors': Errors | None
})


@dataclass
class ResponseData:
    data: RespDataType
    includes: Includes | None
    meta: Meta | None = None
    errors: Errors | None = None

    @classmethod
    def from_dict(cls, data: RawData) -> 'ResponseData':
        return cls(
            data=data.get('data', None),
            includes=Includes.from_dict(data.get('includes', {})),
            meta=Meta.from_dict(data.get('meta', {})),
            errors=Errors.from_dict(data.get('errors', {}))
        )