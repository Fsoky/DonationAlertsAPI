from dataclasses import dataclass
from typing import Any


@dataclass
class Event:

	id: int
	alert_type: str
	is_shown: str
	additional_data: dict
	billing_system: str
	billing_system_type: str
	username: str
	amount: str
	amount_formatted: str
	amount_main: int
	currency: str
	message: str
	header: str
	date_created: Any
	emotes: str
	ap_id: str
	_is_test_alert: bool
	message_type: str
	preset_id: int
	objects: dict


@dataclass
class Donations:

	donation = []
	objects: dict = None


@dataclass
class DonationsData:

	amount: int
	amount_in_user_currency: float
	created_at: Any
	currency: str
	id: int
	is_shown: int
	message: str
	message_type: str
	name: str
	payin_system: str
	recipient_name: str
	shown_at: str
	username: str


@dataclass
class User:

	avatar: str
	code: str
	email: str
	id: int
	language: str
	name: str
	socket_connection_token: str
	objects: dict


@dataclass
class Data:

	access_token: str
	expires_in: int
	refresh_token: str
	token_type: str
	objects: dict


@dataclass
class CentrifugoResponse:

	amount: int
	amount_in_user_currency: float
	created_at: Any
	currency: str
	id: int
	is_shown: int
	message: str
	message_type: str
	name: str
	payin_system: str
	recipient_name: str
	shown_at: str
	username: str
	reason: str
	objects: dict