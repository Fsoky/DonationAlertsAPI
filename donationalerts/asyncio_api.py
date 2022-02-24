import json
from datetime import datetime

import asyncio
import socketio
import aiohttp
import websockets

from .utils import Event, User, Data, Donations, DonationsData, CentrifugoResponse

DEFAULT_URL = "https://www.donationalerts.com/oauth/"
DEFAULT_API_LINK = "https://www.donationalerts.com/api/v1/"


class DonationAlertsAPI:
	
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

	async def get_access_token(self, code, *, full_json=False):
		payload = {
			"client_id": self.client_id,
			"client_secret": self.client_secret,
			"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": self.redirect_uri,
			"scope": self.scope
		}

		async with aiohttp.ClientSession() as session:
			async with session.post(f"{DEFAULT_URL}token", data=payload) as response:
				obj = await response.json()

				return Data(
					obj["access_token"],
					obj["expires_in"],
					obj["refresh_token"],
					obj["token_type"],
					obj
					) if full_json else obj["access_token"]

	async def donations_list(self, access_token, *, page: int=1):
		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/x-www-form-urlencoded"
		}

		async with aiohttp.ClientSession() as session:
			async with session.get(f"{DEFAULT_API_LINK}alerts/donations?page={page}", headers=headers) as response:
				objs = await response.json()
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

	async def user(self, access_token):
		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/x-www-form-urlencoded"
		}

		async with aiohttp.ClientSession() as session:
			async with session.get(f"{DEFAULT_API_LINK}user/oauth", headers=headers) as response:
				obj = await response.json()

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

	async def send_custom_alert(self, access_token, external_id, headline, message, *, image_url=None, sound_url=None, is_shown=0):
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

		async with aiohttp.ClientSession() as session:
			async with session.post(f"{DEFAULT_API_LINK}custom_alert", data=payload, headers=headers) as response:
				return await response.json()

	async def get_refresh_token(self, access_token, refresh_token):
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

		async with aiohttp.ClientSession() as session:
			async with session.post(f"{DEFAULT_URL}token", data=payload, headers=headers) as response:
				obj = await response.json()

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

	async def subscribe(self, channels):
		chnls = [f"{channels}{self.user_id}"]
		if isinstance(channels, list):
			chnls = []
			for channel in channels:
				chnls.append(f"{channel}{self.user_id}")

		async with websockets.connect("wss://centrifugo.donationalerts.com/connection/websocket") as websocket:
			await websocket.send(json.dumps(
				{
					"params": {
						"token": self.socket_connection_token
					},
					"id": self.user_id
				}
			))

			websocket_response = json.loads(await websocket.recv())

			headers = {
				"Authorization": f"Bearer {self.access_token}",
				"Content-Type": "application/json"
			}
			data = {
				"channels": chnls,
				"client": websocket_response["result"]["client"]
			}

			async with aiohttp.ClientSession(headers=headers) as session:
				async with session.post(f"{DEFAULT_API_LINK}centrifuge/subscribe", data=json.dumps(data)) as response:
					response = await response.json()

					for ch in response["channels"]:
						await websocket.send(json.dumps(
							{
								"params": {
									"channel": ch["channel"],
									"token": ch["token"]
								},
								"method": 1,
								"id": self.user_id
							}
						))

					await websocket.recv()
					await websocket.recv()

					obj = json.loads(await websocket.recv())["result"]["data"]["data"]
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


sio = socketio.AsyncClient()


class Alert:

	def __init__(self, token):
		self.token = token

	def event(self):
		def decorate(function):
			async def wrapper():

				@sio.on("connect")
				async def on_connect():
					await sio.emit("add-user", {"token": self.token, "type": "alert_widget"})

				@sio.on("donation")
				async def on_message(data):
					data = json.loads(data)

					await function(
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

				await sio.connect("wss://socket.donationalerts.ru:443", transports="websocket")

			loop = asyncio.get_event_loop()
			loop.run_until_complete(wrapper())
			return loop.run_forever()

		return decorate