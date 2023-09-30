from typing import List

from .models import Scope
from aiohttp import ClientSession


class DonationAlertsAPIBase:

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            scopes: str | List[Scope]
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes

        if isinstance(scopes, list):
            self.scopes = " ".join([scope.value for scope in scopes])


class AIODonationAlertsAPIBase:

    def __init__(
            self,
            client_id: str=None,
            client_secret: str=None,
            redirect_uri: str=None,
            scopes: str | List[Scope]=None
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes

        self.session: ClientSession = ClientSession()

        if isinstance(scopes, list):
            self.scopes = " ".join([scope.value for scope in scopes])