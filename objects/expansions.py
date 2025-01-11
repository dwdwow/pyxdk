from enum import Enum


class PostPayloadExpansion(Enum):
    """Expansions available for Post objects"""
    AUTHOR_ID = "author_id"
    REFERENCED_TWEETS_ID = "referenced_tweets.id" 
    EDIT_HISTORY_TWEET_IDS = "edit_history_tweet_ids"
    IN_REPLY_TO_USER_ID = "in_reply_to_user_id"
    ATTACHMENTS_MEDIA_KEYS = "attachments.media_keys"
    ATTACHMENTS_POLL_IDS = "attachments.poll_ids"
    GEO_PLACE_ID = "geo.place_id"
    ENTITIES_MENTIONS_USERNAME = "entities.mentions.username"
    REFERENCED_TWEETS_AUTHOR_ID = "referenced_tweets.id.author_id"

    @classmethod
    def all_expansions(cls) -> str:
        """Returns comma-separated string of all available expansions"""
        return ",".join([
            cls.AUTHOR_ID.value,
            cls.REFERENCED_TWEETS_ID.value,
            cls.EDIT_HISTORY_TWEET_IDS.value,
            cls.IN_REPLY_TO_USER_ID.value,
            cls.ATTACHMENTS_MEDIA_KEYS.value,
            cls.ATTACHMENTS_POLL_IDS.value,
            cls.GEO_PLACE_ID.value,
            cls.ENTITIES_MENTIONS_USERNAME.value,
            cls.REFERENCED_TWEETS_AUTHOR_ID.value
        ])
        

class UserPayloadExpansion(Enum):
    """Expansions available for User objects"""
    PINNED_TWEET_ID = "pinned_tweet_id"

    @classmethod
    def all_expansions(cls) -> str:
        """Returns comma-separated string of all available expansions"""
        return cls.PINNED_TWEET_ID.value
    

class DirectMessageEventPayloadExpansion(Enum):
    """Expansions available for Direct Message Event objects"""
    ATTACHMENTS_MEDIA_KEYS = "attachments.media_keys"
    REFERENCED_TWEETS_ID = "referenced_tweets.id"
    SENDER_ID = "sender_id"
    PARTICIPANT_IDS = "participant_ids"

    @classmethod
    def all_expansions(cls) -> str:
        """Returns comma-separated string of all available expansions"""
        return ",".join([
            cls.ATTACHMENTS_MEDIA_KEYS.value,
            cls.REFERENCED_TWEETS_ID.value,
            cls.SENDER_ID.value,
            cls.PARTICIPANT_IDS.value
        ])


class SpacePayloadExpansion(Enum):
    """Expansions available for Space objects"""
    INVITED_USER_IDS = "invited_user_ids"
    SPEAKER_IDS = "speaker_ids"
    CREATOR_ID = "creator_id"
    HOST_IDS = "host_ids"
    TOPICS_IDS = "topics_ids"

    @classmethod
    def all_expansions(cls) -> str:
        """Returns comma-separated string of all available expansions"""
        return ",".join([
            cls.INVITED_USER_IDS.value,
            cls.SPEAKER_IDS.value,
            cls.CREATOR_ID.value,
            cls.HOST_IDS.value,
            cls.TOPICS_IDS.value
        ])


class ListPayloadExpansion(Enum):
    """Expansions available for List objects"""
    OWNER_ID = "owner_id"

    @classmethod
    def all_expansions(cls) -> str:
        """Returns comma-separated string of all available expansions"""
        return cls.OWNER_ID.value
