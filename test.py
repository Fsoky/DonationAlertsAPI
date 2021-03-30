from flask import Flask, redirect
from dapi import DonationAlertsApi

client = Flask(__name__)
scopes = "oauth-user-show oauth-custom_alert-store oauth-donation-index oauth-custom_alert-store oauth-goal-subscribe oauth-poll-subscribe"
api = DonationAlertsApi("client id", "client secret", "redirect uri", scopes)


@client.route("/", methods=["get"])
def index():
	return redirect(api.login())


@client.route("/login", methods=["get"])
def login():
	code = api.get_code()
	access_token = api.get_access_token(code)

	user = api.get_user(access_token)
	donate = api.get_donations(access_token)
	
	return user


if __name__ == "__main__":
	client.run(debug=True)