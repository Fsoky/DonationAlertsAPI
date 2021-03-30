import requests
from flask import request


class DonationAlertsApi:

	def __init__(self, client_id, client_secret, redirect_uri, scope):
		symbols = [",", ", ", " ", "%20"]

		for symbol in symbols:
			if symbol in scope:
				self.scope = scope.replace(symbol, "%20").strip()
			else:
				self.scope = scope

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
		link = self.login_url
		return link


	def get_code(self):
		code = request.args.get("code")
		return code


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