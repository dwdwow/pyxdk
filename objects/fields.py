from enum import Enum
from typing import List


class Field(Enum):
    # Post fields
    TWEET = "tweet.fields"
    # User fields
    USER = "user.fields"
    # Trend fields
    TREND = "trend.fields"
    # Space fields
    SPACE = "space.fields"
    # Direct message event fields
    DM_EVENT = "dm_event.fields"
    # Media fields
    MEDIA = "media.fields"
    # Poll fields
    POLL = "poll.fields"
    # Place fields
    PLACE = "place.fields"
    # Community fields
    COMMUNITY = "community.fields"
    # List fields
    LIST = "list.fields"


class TweetField(Enum):
    # default
    ID = "id"
    TEXT = "text"
    EDIT_HISTORY_TWEET_IDS = "edit_history_tweet_ids"
    # optional
    ATTACHMENTS = "attachments"
    AUTHOR_ID = "author_id"
    CONTEXT_ANNOTATIONS = "context_annotations"
    CONVERSATION_ID = "conversation_id"
    CREATED_AT = "created_at"
    EDIT_CONTROLS = "edit_controls"
    ENTITIES = "entities"
    IN_REPLY_TO_USER_ID = "in_reply_to_user_id"
    LANG = "lang"
    NON_PUBLIC_METRICS = "non_public_metrics"
    ORGANIC_METRICS = "organic_metrics"
    POSSIBLY_SENSITIVE = "possibly_sensitive"
    PROMOTED_METRICS = "promoted_metrics"
    PUBLIC_METRICS = "public_metrics"
    REFERENCED_TWEETS = "referenced_tweets"
    REPLY_SETTINGS = "reply_settings"
    WITHHELD = "withheld"
        
    @classmethod
    def optional_fields(cls) -> List[str]:
        return [
            cls.ATTACHMENTS.value,
            cls.AUTHOR_ID.value,
            cls.CONTEXT_ANNOTATIONS.value,
            cls.CONVERSATION_ID.value,
            cls.CREATED_AT.value,
            cls.EDIT_CONTROLS.value,
            cls.ENTITIES.value,
            cls.IN_REPLY_TO_USER_ID.value,
            cls.LANG.value,
            cls.NON_PUBLIC_METRICS.value,
            cls.ORGANIC_METRICS.value,
            cls.POSSIBLY_SENSITIVE.value,
            cls.PROMOTED_METRICS.value,
            cls.PUBLIC_METRICS.value,
            cls.REFERENCED_TWEETS.value,
            cls.REPLY_SETTINGS.value,
            cls.WITHHELD.value
        ]
        

class UserField(Enum):
    # default
    ID = "id"
    NAME = "name" 
    USERNAME = "username"
    # optional
    CONNECTION_STATUS = "connection_status"
    CREATED_AT = "created_at"
    DESCRIPTION = "description"
    ENTITIES = "entities"
    LOCATION = "location"
    PINNED_TWEET_ID = "pinned_tweet_id"
    PROFILE_IMAGE_URL = "profile_image_url"
    PROTECTED = "protected"
    PUBLIC_METRICS = "public_metrics"
    URL = "url"
    VERIFIED = "verified"
    WITHHELD = "withheld"

    @classmethod
    def optional_fields(cls) -> List[str]:
        return [
            cls.CONNECTION_STATUS.value,
            cls.CREATED_AT.value,
            cls.DESCRIPTION.value,
            cls.ENTITIES.value,
            cls.LOCATION.value,
            cls.PINNED_TWEET_ID.value,
            cls.PROFILE_IMAGE_URL.value,
            cls.PROTECTED.value,
            cls.PUBLIC_METRICS.value,
            cls.URL.value,
            cls.VERIFIED.value,
            cls.WITHHELD.value
        ]
        

class MediaField(Enum):
    # default
    MEDIA_KEY = "media_key"
    TYPE = "type"
    # optional
    URL = "url"
    DURATION_MS = "duration_ms"
    HEIGHT = "height"
    NON_PUBLIC_METRICS = "non_public_metrics"
    ORGANIC_METRICS = "organic_metrics"
    PREVIEW_IMAGE_URL = "preview_image_url"
    PROMOTED_METRICS = "promoted_metrics"
    PUBLIC_METRICS = "public_metrics"
    WIDTH = "width"
    ALT_TEXT = "alt_text"
    VARIANTS = "variants"

    @classmethod 
    def optional_fields(cls) -> List[str]:
        return [
            cls.URL.value,
            cls.DURATION_MS.value,
            cls.HEIGHT.value,
            cls.NON_PUBLIC_METRICS.value,
            cls.ORGANIC_METRICS.value,
            cls.PREVIEW_IMAGE_URL.value,
            cls.PROMOTED_METRICS.value,
            cls.PUBLIC_METRICS.value,
            cls.WIDTH.value,
            cls.ALT_TEXT.value,
            cls.VARIANTS.value
        ]


class PollField(Enum):
    # default
    ID = "id"
    OPTIONS = "options"
    # optional
    DURATION_MINUTES = "duration_minutes"
    END_DATETIME = "end_datetime"
    VOTING_STATUS = "voting_status"

    @classmethod
    def optional_fields(cls) -> List[str]:
        return [
            cls.DURATION_MINUTES.value,
            cls.END_DATETIME.value,
            cls.VOTING_STATUS.value
        ]


class PlaceField(Enum):
    # default
    FULL_NAME = "full_name"
    ID = "id"
    # optional
    CONTAINED_WITHIN = "contained_within"
    COUNTRY = "country"
    COUNTRY_CODE = "country_code"
    GEO = "geo"
    NAME = "name"
    PLACE_TYPE = "place_type"

    @classmethod
    def optional_fields(cls) -> List[str]:
        return [
            cls.CONTAINED_WITHIN.value,
            cls.COUNTRY.value,
            cls.COUNTRY_CODE.value,
            cls.GEO.value,
            cls.NAME.value,
            cls.PLACE_TYPE.value
        ]


class CommunityField(Enum):
    # default
    ID = "id"
    NAME = "name"
    DESCRIPTION = "description"
    JOIN_POLICY = "join_policy"
    ACCESS = "access"
    MEMBER_COUNT = "member_count"
    CREATED_AT = "created_at"

    @classmethod
    def optional_fields(cls) -> List[str]:
        return [
            cls.ID.value,
            cls.NAME.value,
            cls.DESCRIPTION.value,
            cls.JOIN_POLICY.value,
            cls.ACCESS.value,
            cls.MEMBER_COUNT.value,
            cls.CREATED_AT.value
        ]


class ListField(Enum):
    # default
    CREATED_AT = "created_at"
    FOLLOWER_COUNT = "follower_count"
    MEMBER_COUNT = "member_count"
    PRIVATE = "private"
    DESCRIPTION = "description"
    OWNER_ID = "owner_id"