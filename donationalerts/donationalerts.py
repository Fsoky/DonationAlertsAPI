import json
import requests
from datetime import datetime

from websocket import create_connection
import socketio

from .utils import Event, User, Data, Donations, DonationsData, CentrifugoResponse

DEFAULT_URL = "https://www.donationalerts.com/oauth/"
DEFAULT_API_LINK = "https://www.donationalerts.com/api/v1/"


class DonationAlertsAPI:
	"""
	This class describes work with Donation Alerts API
	"""

	def __init__(self, client_id, client_secret, redirect_uri, scopes):
		symbols = [",", ", ", " ", "%20"]

		if isinstance(scopes, list):
			obj_scopes = []
			for scope in scopes:
				obj_scopes.append(scope)

			scopes = " ".join(obj_scopes)
			
		for symbol in symbols:
			if symbol in scopes:
				self.scope = scopes.replace(symbol, "%20").strip() # Replaces some symbols on '%20' for stable work
			else:
				self.scope = scopes

		self.client_id = client_id
		self.client_secret = client_secret
		self.redirect_uri = redirect_uri

	def login(self):
		return f"{DEFAULT_URL}authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scope}"

	def get_access_token(self, code, *, full_json=False):
		payload = {
			"client_id": self.client_id,
			"client_secret": self.client_secret,
			"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": self.redirect_uri,
			"scope": self.scope
		}

		obj = requests.post(f"{DEFAULT_URL}token", data=payload).json()

		return Data(
			obj["access_token"],
			obj["expires_in"],
			obj["refresh_token"],
			obj["token_type"],
			obj
			) if full_json else obj["access_token"]

	def donations_list(self, access_token, *, page: int=1):
		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/x-www-form-urlencoded"
		}

		objs = requests.get(f"{DEFAULT_API_LINK}alerts/donations?page={page}", headers=headers).json()
		donations = Donations(objects=objs)

		for obj in objs["data"]:
			donation_object = DonationsData(
				obj["amount"],
				obj["amount_in_user_currency"],
				datetime.strptime(obj["created_at"], "%Y-%m-%d %H:%M:%S"),
				obj["currency"],
				obj["id"],
				obj["is_shown"],
				obj["message"],
				obj["message_type"],
				obj["name"],
				obj["payin_system"],
				obj["recipient_name"],
				obj["shown_at"],
				obj["username"]
			)
			donations.donation.append(donation_object)

		return donations

	def user(self, access_token):
		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/x-www-form-urlencoded"
		}
		obj = requests.get(f"{DEFAULT_API_LINK}user/oauth", headers=headers).json()

		return User(
			obj["data"]["avatar"],
			obj["data"]["code"],
			obj["data"]["email"],
			obj["data"]["id"],
			obj["data"]["language"],
			obj["data"]["name"],
			obj["data"]["socket_connection_token"],
			obj["data"]
		)

	def send_custom_alert(self, access_token, external_id, headline, message, *, image_url=None, sound_url=None, is_shown=0):
		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/x-www-form-urlencoded"
		}
		payload = {
			"external_id": external_id,
			"headline": headline,
			"message": message,
			"is_shown": is_shown,
			"image_url": image_url,
			"sound_url": sound_url
		}

		obj = requests.post(f"{DEFAULT_API_LINK}custom_alert", data=payload, headers=headers).json()
		return obj

	def get_refresh_token(self, access_token, refresh_token):
		headers = {
			"Content-Type": "application/x-www-form-urlencoded"
		}
		payload = {
			"grant_type": "refresh_token",
			"client_id": self.client_id,
			"client_secret": self.client_secret,
			"refresh_token": refresh_token,
			"redirect_uri": self.redirect_uri,
			"scope": self.scope
		}

		obj = requests.post(f"{DEFAULT_URL}token", data=payload, headers=headers).json()
		return Data(
			obj["access_token"],
			obj["expires_in"],
			obj["refresh_token"],
			obj["token_type"],
			obj
		)


class Centrifugo:

	def __init__(self, socket_connection_token, access_token, user_id):
		self.socket_connection_token = socket_connection_token
		self.access_token = access_token
		self.user_id = user_id

		self.uri = "wss://centrifugo.donationalerts.com/connection/websocket"

	def subscribe(self, channels):
		chnls = [f"{channels}{self.user_id}"]
		if isinstance(channels, list):
			chnls = []
			for channel in channels:
				chnls.append(f"{channel}{self.user_id}")

		ws = create_connection(self.uri)
		ws.send(json.dumps(
			{
				"params": {
					"token": self.socket_connection_token
				},
				"id": self.user_id
			}
		))

		ws_response = json.loads(ws.recv())

		headers = {
			"Authorization": f"Bearer {self.access_token}",
			"Content-Type": "application/json"
		}
		data = {
			"channels": chnls,
			"client": ws_response["result"]["client"]
		}
		
		response = requests.post(f"{DEFAULT_API_LINK}centrifuge/subscribe", data=json.dumps(data), headers=headers).json()
		for ch in response["channels"]:
			self.ws.send(json.dumps(
				{
					"params": {
						"channel": ch["channel"],
						"token": ch["token"]
					},
					"method": 1,
					"id": self.user_id
				}
			))
	
		ws.recv()
		ws.recv()

		obj = json.loads(ws.recv())["result"]["data"]["data"]
		return CentrifugoResponse(
			obj["amount"],
			obj["amount_in_user_currency"],
			datetime.strptime(obj["created_at"], "%Y-%m-%d %H:%M:%S"),
			obj["currency"],
			obj["id"],
			obj["is_shown"],
			obj["message"],
			obj["message_type"],
			obj["name"],
			obj["payin_system"],
			obj["recipient_name"],
			obj["shown_at"],
			obj["username"],
			obj["reason"],
			obj
		)


sio = socketio.Client()


class Alert:

	def __init__(self, token):
		self.token = token

	def event(self):
		def wrapper(function):

			@sio.on("connect")
			def on_connect():
				sio.emit("add-user", {"token": self.token, "type": "alert_widget"})

			@sio.on("donation")
			def on_message(data):
				data = json.loads(data)

				function(
					Event(
						data["id"],
						data["alert_type"],
						data["is_shown"],
						json.loads(data["additional_data"]),
						data["billing_system"],
						data["billing_system_type"],
						data["username"],
						data["amount"],
						data["amount_formatted"],
						data["amount_main"],
						data["currency"],
						data["message"],
						data["header"],
						datetime.strptime(data["date_created"], "%Y-%m-%d %H:%M:%S"),
						data["emotes"],
						data["ap_id"],
						data["_is_test_alert"],
						data["message_type"],
						data["preset_id"],
						data
					)
				)

			sio.connect("wss://socket.donationalerts.ru:443", transports="websocket")

		return wrapper