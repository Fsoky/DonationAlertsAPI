import requests
import json
from flask import request
from websocket import create_connection


class Scopes:

	user_show = "oauth-user-show"

	donation_subscribe = "oauth-donation-subscribe"
	donation_index = "oauth-donation-index"

	custom_alert_store = "oauth-custom_alert-store"

	goal_subscribe = "oauth-goal-subscribe"
	poll_subscribe = "oauth-poll-subscribe"

	all_scopes = [user_show, donation_subscribe, donation_index, custom_alert_store,
					goal_subscribe, poll_subscribe]


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
		self.token_url = f"https://www.donationalerts.com/oauth/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code="

		# API LINKS
		self.user_api = "https://www.donationalerts.com/api/v1/user/oauth"
		self.donations_api = "https://www.donationalerts.com/api/v1/alerts/donations"
		self.custom_alerts_api = "https://www.donationalerts.com/api/v1/custom_alert"


	def login(self):
		return self.login_url


	def get_code(self):
		return request.args.get("code")


	def get_access_token(self, code):
		payload = {
			"client_id": self.client_id,
			"client_secret": self.client_secret,
			"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": self.redirect_uri,
			"scope": self.scope
		}

		access_token = requests.post(url=self.token_url, data=payload).json()
		return access_token.get("access_token")


	def get_donations(self, access_token):
		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/x-www-form-urlencoded"
		}
		donate_object = requests.get(url=self.donations_api, headers=headers).json()

		return donate_object # HERE PROBLEMS!!!


	def get_user(self, access_token):
		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/x-www-form-urlencoded"
		}
		user_object = requests.get(url=self.user_api, headers=headers).json()

		return user_object


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

	def subscribe(self):
		headers = {
			"Authorization": f"Bearer {self.access_token}",
			"Content-Type": "application/json"
		}
		data = {
			"channels": [f"$alerts:donation_{self.user_id}"],
			"client": self.ws_response["result"]["client"]
		}

		response = requests.post(url="https://www.donationalerts.com/api/v1/centrifuge/subscribe", data=json.dumps(data), headers=headers).json()

		self.ws.send(json.dumps(
			{
				"params": {
					"channel": f"$alerts:donation_{self.user_id}",
					"token": response["channels"][0]["token"]
				},
				"method": 1,
				"id": self.user_id
			}
		))

		return json.loads(self.ws.recv())