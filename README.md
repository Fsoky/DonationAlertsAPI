# Donation-Alerts-API-Python
This module for python. With help this module, you can interact with API Donation Alerts

`pip install donationalerts_api -U`

[PyPi](https://pypi.org/project/donationalerts-api/)

[Official documentation Donation alerts API](https://www.donationalerts.com/apidoc)

[Donation alerts application clients](https://www.donationalerts.com/application/clients)


|Main class|Description|
|----------|-----------|
|DonationAlertsApi(client_id, client_secret, redirect_uri, scope)|Request to API Donation Alerts|

|Method|Description|
|------|-----------|
|login()|Returns link for connect to API|
|get_code()|Returns code access application|
|get_access_token(code)|Receive access token for the application (necessarily: transfer argument code which you got by get_code)|
|get_donations(access_token)|Receive information about donate (messages)|
|get_user(access_token)|Receive information about user|
|send_custom_alert(access_token, external_id, headline, messages, image_url=None, sound_url=None, is_shown=0)|Send custom alert|


### Example:
```py
from flask import Flask, redirect
from donationalerts_api import DonationAlertsApi

client = Flask(__name__)
api = DonationAlertsApi("9999", "a43f67k9920h01a2wdw", "http://127.0.0.1:5000/login", "scopes")


@client.route("/", methods=["get"])
def index():
  redirect(api.login())
  

@client.route("/login", methods=["get"])
def login():
  code = api.get_code()
  access_token = api.get_access_token(code)
  
  user = api.get_user(access_token)
  donations = api.get_donations(access_token)
  
  api.send_custom_alert(access_token, 12, "Test headline", "Test something message...")
  
  return user
  
  
if __name__ == "__main__":
  client.run(debug=True)
```