from typing import List, Optional, Any, Dict
from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class Scope(Enum):
    OAUTH_USER_SHOW: str = "oauth-user-show"
    OAUTH_DONATION_SUBSCRIBE: str = "oauth-donation-subscribe"
    OAUTH_DONATION_INDEX: str = "oauth-donation-index"
    OAUTH_CUSTOM_ALERT_STORE: str = "oauth-custom_alert-store"
    OAUTH_GOAL_SUBSCRIBE: str = "oauth-goal-subscribe"
    OAUTH_POLL_SUBSCRIBE: str = "oauth-poll-subscribe"

    def __repr__(self):
        return self.value
    
    @classmethod
    def all_scopes(cls) -> List[str]:
        return list(cls)
    

class CentrifugoChannel(Enum):
    NEW_DONATION_ALERTS: str = "$alerts:donation_"
    DONATION_GOALS_UPDATES: str = "$goals:goal_"
    POLLS_UPDATES: str = "$poll:poll_"

    def __repr__(self) -> str:
        return self.value
    
    @classmethod
    def all_channels(cls) -> List[str]:
        return list(cls)


class AccessToken(BaseModel):
    token_type: str
    access_token: str
    expires_in: int
    refresh_token: str


class DonationsData(BaseModel):
    id: int
    name: str
    username: str
    message_type: str
    message: str
    amount: int
    currency: str
    is_shown: int
    created_at: datetime
    shown_at: Optional[str] | None


class DonationsLinks(BaseModel):
    first: str
    last: str
    prev: Optional[Any] | None = None
    next: Optional[Any] | None = None


class DonationsMeta(BaseModel):
    current_page: int
    from_page: int
    last_page: int
    path: str
    per_page: int
    to: int
    total: int


class Donations(BaseModel):
    items: List[DonationsData]
    links: Dict[str, DonationsLinks]
    meta: Dict[str, DonationsMeta]
    

class User(BaseModel):
    id: int
    code: str
    name: str
    avatar: str
    email: str
    is_active: int
    language: str
    socket_connection_token: str


class CustomAlert(BaseModel):
    id: int
    external_id: Optional[int] | None
    header: Optional[str] | None
    message: Optional[str] | None
    image_url: Optional[str] | None
    sound_url: Optional[str] | None
    is_shown: int
    created_at: datetime
    shown_at: Optional[str] | None


class CentrifugoEventResponse(BaseModel):
    pass