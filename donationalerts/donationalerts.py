from api.get_api import (
    DonationAlertsAPIAuthorize,
    DonationAlertsAPIDonations,
    DonationAlertsAPIUser,
    DonationAlertsAPICustomAlert
)
from api.get_async_api import (
    AIODonationAlertsAPIAuthorize,
    AIODonationAlertsAPIUser,
    AIODonationAlertsAPIDonations,
    AIODonationAlertsAPICustomAlert
)

from utils.base import DonationAlertsAPIBase, AIODonationAlertsAPIBase
from utils.models import Scope


class DonationAlertsAPI(DonationAlertsAPIBase):

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            scopes: str | list[Scope]
    ) -> None:
        super().__init__(
            client_id,
            client_secret,
            redirect_uri,
            scopes
        )
    
    @property
    def authorize(self) -> DonationAlertsAPIAuthorize:
        return DonationAlertsAPIAuthorize(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
            self.scopes
        )
    
    @property
    def donations(self) -> DonationAlertsAPIDonations:
        return DonationAlertsAPIDonations()
    
    @property
    def user(self) -> DonationAlertsAPIUser:
        return DonationAlertsAPIUser()
    
    @property
    def custom_alert(self) -> DonationAlertsAPICustomAlert:
        return DonationAlertsAPICustomAlert()


class AIODonationAlertsAPI(AIODonationAlertsAPIBase):
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            scopes: str | list[Scope]
    ) -> None:
        super().__init__(
            client_id,
            client_secret,
            redirect_uri,
            scopes
        )

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        return self.session.close()

    @property
    async def authorize(self) -> AIODonationAlertsAPIAuthorize:
        return AIODonationAlertsAPIAuthorize(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
            self.scopes
        )
    
    @property
    async def donations(self) -> AIODonationAlertsAPIDonations:
        return AIODonationAlertsAPIDonations()

    @property
    async def user(self) -> AIODonationAlertsAPIUser:
        return AIODonationAlertsAPIUser()
    
    @property
    async def custom_alert(self) -> AIODonationAlertsAPICustomAlert:
        return AIODonationAlertsAPICustomAlert()