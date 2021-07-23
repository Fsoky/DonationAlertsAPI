from flask import Flask, redirect
from donationalerts_api import DonationAlertsApi, Scopes, Centrifugo

app = Flask(__name__)
api = DonationAlertsApi("client id", "client secret", "http://127.0.0.1:5000/login", Scopes.all_scopes)


@app.route("/", methods=["get"])
def index():
  return redirect(api.login())
  

@app.route("/login", methods=["get"])
def login():
  """Beta ~"""

  code = api.get_code()

  access_token = api.get_access_token(code)
  socket_token = api.get_user(access_token)["data"]["socket_connection_token"]
  user_id = api.get_user(access_token)["data"]["id"]

  fugo = Centrifugo(socket_token, access_token, user_id)
  fugo.connect()

  return fugo.subscribe()

if __name__ == "__main__":
  app.run(debug=True)