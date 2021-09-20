from flask import Flask, redirect, request

from donationalerts_api import DonationAlertsAPI, Centrifugo
from donationalerts_api.modules import Scopes, Channels

app = Flask(__name__)
api = DonationAlertsAPI("client id", "client secret", "http://127.0.0.1:5000/login", [Scopes.USER_SHOW, Scopes.DONATION_SUBSCRIBE])


@app.route("/", methods=["get"])
def index():
	return redirect(api.login()) # Log in your application


@app.route("/login", methods=["get"])
def login():
	code = request.args.get("code")
	access_token = api.get_access_token(code)
	user = api.user(access_token)

	fugo = Centrifugo(user.socket_connection_token, access_token, user.id)
	event = fugo.subscribe(Channels.NEW_DONATION_ALERTS)

	return event.objects


if __name__ == "__main__":
	app.run(debug=True)