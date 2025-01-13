from dataclasses import dataclass
from typing import TypeVar, TypedDict
from objects.community import Community
from objects.direct_msg_events import DirectMessageEvent
from objects.errors import Errors
from objects.xlist import List
from objects.media import Media
from objects.meta import Meta
from objects.place import Place
from objects.poll import Poll
from objects.space import Space
from objects.tweet import Tweet
from objects.user import User


# DataItem = TypeVar('DataItem', Tweet, User, Space, List, Media, Poll, Place, Community, DirectMessageEvent)
# RespDataType = TypeVar('RespDataType', list[DataItem], DataItem, None)


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

    @classmethod
    def from_dict(cls, data: dict) -> 'Includes':
        if not data:
            return None
        return cls(
            tweets=data.get('tweets', None),
            users=data.get('users', None),
            spaces=data.get('spaces', None),
            lists=data.get('lists', None),
            media=data.get('media', None),
            polls=data.get('polls', None),
            places=data.get('places', None),
            communities=data.get('communities', None),
            direct_message_events=data.get('direct_message_events', None),
            meta=data.get('meta', None)
        )
    
    
# RawData = TypedDict('RawData', {
#     'data': RespDataType,  
#     'includes': Includes | None,
#     'meta': Meta | None,
#     'errors': Errors | None
# })


@dataclass
class ResponseData[D]:
    data: D
    includes: Includes | None
    meta: Meta | None = None
    errors: Errors | None = None

    @classmethod
    def from_dict[D](cls, data: dict) -> 'ResponseData[D]':
        return cls(
            data=data.get('data'),
            includes=Includes.from_dict(data.get('includes')),
            meta=Meta.from_dict(data.get('meta')),
            errors=Errors.from_dict(data.get('errors'))
        )