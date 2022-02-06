from donationalerts_api.asyncio_api import Alert

import os

alert = Alert(os.getenv('DONATIONALERTS_TOKEN'))


@alert.event()
async def new_donation(event):
	print(event)

alert.run()