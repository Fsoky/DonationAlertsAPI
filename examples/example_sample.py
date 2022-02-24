from flask import Flask, redirect, request
from donationalerts_api import DonationAlertsAPI, Scopes

app = Flask(__name__)
api = DonationAlertsAPI("client id", "client secret", "http://127.0.0.1:5000/login", [Scopes.USER_SHOW, Scopes.DONATION_INDEX])


@app.route("/", methods=["get"])
def index():
	return redirect(api.login()) # Log in your application


@app.route("/login", methods=["get"])
def login():
	code = request.args.get("code")
	access_token = api.get_access_token(code)

	user = api.user(access_token)
	donation_list = api.donations_list(access_token)

	return user.objects


if __name__ == "__main__":
	app.run(debug=True)