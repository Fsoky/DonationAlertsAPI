import requests
import json
from flask import request
from websocket import create_connection


class Scopes:

	USER_SHOW = "oauth-user-show"

	DONATION_SUBSCRIBE = "oauth-donation-subscribe"
	DONATION_INDEX = "oauth-donation-index"

	CUSTOM_ALERT_STORE = "oauth-custom_alert-store"

	GOAL_SUBSCRIBE = "oauth-goal-subscribe"
	POLL_SUBSCRIBE = "oauth-poll-subscribe"

	ALL_SCOPES = [USER_SHOW, DONATION_INDEX, DONATION_SUBSCRIBE, CUSTOM_ALERT_STORE,
					GOAL_SUBSCRIBE, POLL_SUBSCRIBE]


class Channels:

	NEW_DONATION_ALERTS = "$alerts:donation_"

	DONATION_GOALS_UPDATES = "$goals:goal_"

	POLLS_UPDATES = "$polls:poll_"

	ALL_CHANNELS = [NEW_DONATION_ALERTS, DONATION_GOALS_UPDATES, POLLS_UPDATES]


class DonationAlertsApi:
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
		self.login_url = f"https://www.donationalerts.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={self.scope}"
		self.token_url = f"https://www.donationalerts.com/oauth/token"

		# API LINKS
		self.user_api = "https://www.donationalerts.com/api/v1/user/oauth"
		self.donations_api = "https://www.donationalerts.com/api/v1/alerts/donations"
		self.custom_alerts_api = "https://www.donationalerts.com/api/v1/custom_alert"

	def login(self):
		return self.login_url

	def get_code(self):
		return request.args.get("code")

	def get_access_token(self, code, full=False):
		payload = {
			"client_id": self.client_id,
			"client_secret": self.client_secret,
			"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": self.redirect_uri,
			"scope": self.scope
		}

		access_token = requests.post(url=self.token_url, data=payload).json()
		self.refresh_token = access_token.get("refresh_token")

		return access_token if full else access_token.get("access_token")

	def get_donations(self, access_token):
		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/x-www-form-urlencoded"
		}
		donate_object = requests.get(url=self.donations_api, headers=headers).json()

		return donate_object

	def get_user(self, access_token):
		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/x-www-form-urlencoded"
		}
		user_object = requests.get(url=self.user_api, headers=headers).json()

		return user_object["data"]

	def send_custom_alert(self, access_token, external_id, headline, message, image_url=None, sound_url=None, is_shown=0):
		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/x-www-form-urlencoded"
		}
		data = {
			"external_id": external_id,
			"header": headline,
			"message": message,
			"is_shown": is_shown,
			"image_url": image_url,
			"sound_url": sound_url
		}
		custom_alert_object = requests.post(url=self.custom_alerts_api, data=data, headers=headers).json()

		return custom_alert_object

	def get_refresh_token(self):
		headers = {"Content-Type": "application/x-www-form-urlencoded"}
		data = {
			"grant_type": "refresh_token",
			"client_id": self.client_id,
			"client_secret": self.client_secret,
			"refresh_token": self.refresh_token,
			"redirect_uri": self.redirect_uri,
			"scope": self.scope
		}

		response = requests.post(url=self.token_url, data=data, headers=headers).json()
		return response


class Centrifugo:

	def __init__(self, socket_connection_token, access_token, user_id):
		self.socket_connection_token = socket_connection_token
		self.access_token = access_token
		self.user_id = user_id

		self.uri = "wss://centrifugo.donationalerts.com/connection/websocket"

	def connect(self):
		self.ws = create_connection(self.uri)
		self.ws.send(json.dumps(
			{
				"params": {
					"token": self.socket_connection_token
				},
				"id": self.user_id
			}
		))
		self.ws_response = json.loads(self.ws.recv())

		return self.ws_response

	def subscribe(self, channels):
		chnls = [f"{channels}{self.user_id}"]

		if isinstance(channels, list):
			chnls = []
			for channel in channels:
				chnls.append(f"{channel}{self.user_id}")

		headers = {
			"Authorization": f"Bearer {self.access_token}",
			"Content-Type": "application/json"
		}
		data = {
			"channels": chnls,
			"client": self.ws_response["result"]["client"]
		}
		
		response = requests.post(url="https://www.donationalerts.com/api/v1/centrifuge/subscribe", data=json.dumps(data), headers=headers).json()
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
	
		answer = {"response": self.ws.recv(), "sec_response": self.ws.recv()}
		return answer

	def listen(self):
		return json.loads(self.ws.recv())["result"]["data"]["data"]