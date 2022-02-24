from donationalerts import Alert

alert = Alert("token")


@alert.event()
def new_donation(event):
	print(event)