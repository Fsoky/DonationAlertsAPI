from datetime import datetime
from typing import List, Dict, Any, Optional

from urllib.parse import urlencode, quote
from requests import Response, post, get

from utils.base import DonationAlertsAPIBase
from utils.models import (
    Scope,
    AccessToken,
    DonationsData,
    Donations,
    User,
    CustomAlert
)

DEFAULT_URL = "https://www.donationalerts.com/oauth/"
DEFAULT_API_LINK = "https://www.donationalerts.com/api/v1/"


class DonationAlertsAPIAuthorize(DonationAlertsAPIBase):

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            scopes: str | List[Scope]
    ) -> None:
        super().__init__(
            client_id,
            client_secret,
            redirect_uri,
            scopes
        )
    
    def login(self) -> str:
        payload: Dict[str, Any] = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": self.scopes
        }

        return f"{DEFAULT_URL}authorize?{urlencode(payload, quote_via=quote)}"

    def get_access_token(self, code: str) -> AccessToken:
        payload: Dict[str, Any] = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
        }
        response: Response = post(f"{DEFAULT_URL}token", data=payload)

        return AccessToken(**response.json())
    
    def refresh_access_token(self, refresh_token: str) -> AccessToken:
        headers: Dict[str, Any] = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload: Dict[str, Any] = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.scopes
        }
        response: Response = post(
            f"{DEFAULT_URL}token",
            headers=headers,
            data=payload
        )

        return AccessToken(**response.json())


class DonationAlertsAPIDonations:
    
    def __init__(self) -> None:
        pass

    def get(self, access_token: str, page: int=1) -> Donations:
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response: Response = get(
            f"{DEFAULT_API_LINK}alerts/donations?page={page}",
            headers=headers
        )

        donations: DonationsData = [
            DonationsData(
                created_at=datetime.strptime(item["created_at"], "%Y-%m-%d %H:%M:%S"),
                **{key: value for key, value in item.items() if key != "created_at"}
            )
            if "created_at" in item and isinstance(item["created_at"], str)
            else DonationsData(**item)
            for item in response.json()["data"]
        ]

        return Donations(items=donations, links=response.json()["links"], meta=response.json()["meta"])


class DonationAlertsAPIUser:

    def __init__(self) -> None:
        pass

    def get(self, access_token: str) -> User:
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response: Response = get(
            f"{DEFAULT_API_LINK}user/oauth",
            headers=headers
        )

        return User(**response.json()["data"])


class DonationAlertsAPICustomAlert:

    def __init__(self) -> None:
        pass

    def send(
            self,
            access_token: str,
            external_id: str,
            header: str,
            message: str,
            *,
            is_shown: int=0,
            image_url: Optional[str] | None=None,
            sound_url: Optional[str] | None=None
    ) -> CustomAlert:
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload: Dict[str, Any] = {
            "external_id": external_id,
            "header": header,
            "message": message,
            "is_shown": is_shown,
            "image_url": image_url,
            "sound_url": sound_url
        }
        response: Response = post(
            f"{DEFAULT_API_LINK}custom_alert",
            headers=headers,
            data=payload
        )

        return CustomAlert(**response.json()["data"])