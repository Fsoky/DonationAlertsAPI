from datetime import datetime
from typing import List, Dict, Any, Optional

from urllib.parse import urlencode, quote

from .get_api import DEFAULT_URL, DEFAULT_API_LINK

from utils.base import AIODonationAlertsAPIBase
from utils.models import (
    Scope,
    AccessToken,
    DonationsData,
    Donations,
    User,
    CustomAlert
)


class AIODonationAlertsAPIAuthorize(AIODonationAlertsAPIBase):

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

    async def login(self) -> str:
        payload: Dict[str, Any] = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": self.scopes
        }

        return f"{DEFAULT_URL}authorize?{urlencode(payload, quote_via=quote)}"
    
    async def get_access_token(self, code: str) -> AccessToken:
        payload: Dict[str, Any] = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
        }
        
        async with self.session.post(f"{DEFAULT_URL}token", data=payload) as response:
            response_obj: Dict[str, Any] = await response.json()
            return AccessToken(**response_obj)
        
    async def refresh_access_token(self, refresh_token: str) -> AccessToken:
        headers: Dict[str, str] = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload: Dict[str, Any] = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.scopes
        }

        async with self.session.post(f"{DEFAULT_URL}token", headers=headers, data=payload) as response:
            response_obj: Dict[str, Any] = await response.json()
            return AccessToken(**response_obj)


class AIODonationAlertsAPIUser(AIODonationAlertsAPIBase):

    def __init__(self) -> None:
        pass

    async def get(self, access_token: str) -> User:
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        async with self.session.get(f"{DEFAULT_API_LINK}user/oauth", headers=headers) as response:
            response_obj: Dict[str, Any] = await response.json()
            return User(**response_obj)


class AIODonationAlertsAPIDonations(AIODonationAlertsAPIBase):

    def __init__(self) -> None:
        pass

    async def get(self, access_token: str, page: int=1) -> Donations:
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        async with self.session.get(f"{DEFAULT_API_LINK}alerts/donations?page={page}", headers=headers) as response:
            response_obj: Dict[str, Any] = await response.json()
            donations: DonationsData = [
                DonationsData(
                    created_at=datetime.strptime(item["created_at"], "%Y-%m-%d %H:%M:%S"),
                    **{key: value for key, value in item.items() if key != "created_at"}
                )
                if "created_at" in item and isinstance(item["created_at"], str)
                else DonationsData(**item)
                for item in response_obj["data"]
            ]

            return Donations(items=donations, links=response_obj["links"], meta=response_obj["meta"])
        

class AIODonationAlertsAPICustomAlert(AIODonationAlertsAPIBase):

    def __init__(self) -> None:
        pass

    async def send(
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
        
        async with self.session.post(f"{DEFAULT_API_LINK}custom_alert", headers=headers, data=payload) as response:
            response_obj: Dict[str, Any] = await response.json()
            return CustomAlert(**response_obj["data"])