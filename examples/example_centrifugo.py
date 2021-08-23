from flask import Flask, redirect
from donationalerts_api import DonationAlertsApi, Centrifugo, Scopes, Channels

app = Flask(__name__)
api = DonationAlertsApi("client id", "client secret", "http://127.0.0.1:5000/login", [Scopes.USER_SHOW, Scopes.DONATION_SUBSCRIBE])


@app.route("/", methods=["get"])
def index():
	return redirect(api.login()) # Log in your application


@app.route("/login", methods=["get"])
def login():
	code = api.get_code()
	access_token = api.get_access_token(code)
	user = api.get_user(access_token)

	fugo = Centrifugo(user["socket_connection_token"], access_token, user["id"])
	fugo.connect()
	fugo.subscribe(Channels.NEW_DONATION_ALERTS)

	return fugo.listen()

if __name__ == "__main__":
	app.run(debug=True)