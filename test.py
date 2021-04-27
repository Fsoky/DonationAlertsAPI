from flask import Flask, redirect
from donationalerts_api import DonationAlertsApi, Scopes

client = Flask(__name__)
api = DonationAlertsApi("client id", "client secret", "http://127.0.0.1/login", [Scopes.user_show, Scopes.donation_index])


@client.route("/", methods=["get"])
def index():
	return redirect(api.login())


@client.route("/login", methods=["get"])
def login():
	code = api.get_code()
	access_token = api.get_access_token(code)

	user = api.get_user(access_token)
	return user


if __name__ == "__main__":
	client.run(debug=True)