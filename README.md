# Donation-Alerts-API-Python
This module for python. With help this module, you can interact with API Donation Alerts

    pip install donationalerts_api -U

[PyPi](https://pypi.org/project/donationalerts-api/)

[Official documentation Donation alerts API](https://www.donationalerts.com/apidoc)

[Donation alerts application clients](https://www.donationalerts.com/application/clients)


|Class|Description|
|----------|-----------|
|DonationAlertsApi(client_id, client_secret, redirect_uri, scope)|Request to API Donation Alerts|
|Scopes|Has attributes for the instruction of scopes (USER_SHOW, DONATION_INDEX, DONATION_SUBSCRIBE, CUSTOM_ALERT_STORE, GOAL_SUBSCRIBE, POLL_SUBSCRIBE, ALL_SCOPES)|
|Channels|Has attributes for the subscribe to channels (NEW_DONATION_ALERTS, DONATION_GOALS_UPDATES, POLLS_UPDATES, ALL_CHANNELS)|
|Centrifugo(socket_connection_token, access_token, user_id)|Work with centrifugo|
|Alert(token)|Recieve donation in real-time without Oauth2|

|Method|Description|
|------|-----------|
|login()|Returns link for connect to API|
|get_code()|Returns code access application|
|get_access_token(code, full=False)|Receive access token for the application (necessarily: transfer argument code which you got by get_code, if full=True - returns all json object)|
|get_donations(access_token)|Receive information about donate (messages)|
|get_user(access_token)|Receive information about user|
|send_custom_alert(access_token, external_id, headline, messages, image_url=None, sound_url=None, is_shown=0)|Send custom alert|
|connect()|Connect to centrifugo websocket server|
|subscribe(channels)|Subscribe to centrifugo channels|
|listen()|Recieve response from the server|


### Example:
```py
from flask import Flask, redirect
from donationalerts_api import DonationAlertsApi, Scopes

app = Flask(__name__)
api = DonationAlertsApi("client id", "client secret", "http://127.0.0.1:5000/login", Scopes.ALL_SCOPES)


@app.route("/", methods=["get"])
def index():
  return redirect(api.login())
  

@app.route("/login", methods=["get"])
def login():
  code = api.get_code()
  access_token = api.get_access_token(code)

  user = api.get_user(access_token)
  return user

if __name__ == "__main__":
  app.run(debug=True)
```

## Now you can pass list of scopes:

```py
from donationalerts_api import DonationAlertsApi, Scopes # New class: Scopes

scopes = ["oauth-user-show", "oauth-donation-index", "oauth-poll-subscribe"] # Also right variant
api = DonationAlertsApi("client id", "client secret", "redirect uri", [Scopes.USER_SHOW, Scopes.DONATION_INDEX]) # Or you can pass all scopes: Scopes.ALL_SCOPES
```

## Centrifugo, new events in real-time

```py
from flask import Flask, redirect
from donationalerts_api import DonationAlertsApi, Centrifugo, Scopes, Channels

app = Flask(__name__)
api = DonationAlertsApi("client id", "client secret", "http://127.0.0.1:5000/login", Scopes.ALL_SCOPES)


@app.route("/", methods=["get"])
def index():
  return redirect(api.login())


@app.route("/login", methods=["get"])
def login():
  code = api.get_code()

  access_token = api.get_access_token(code)
  socket_token = api.get_user(access_token)["socket_connection_token"]
  user_id = api.get_user(access_token)["id"]

  fugo = Centrifugo(socket_token, access_token, user_id)
  fugo.connect()
  fugo.subscribe(Channels.NEW_DONATION_ALERTS)

  event = fugo.listen()
  return event

if __name__ == "__main__":
  app.run(debug=True)
```

## New donations in real-time without Oauth2



```py
from donationalerts_api import Alert

alert = Alert("token")

@alert.event()
def new_donation(event):
  print(event)
```
