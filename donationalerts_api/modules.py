class Scopes:
	USER_SHOW = "oauth-user-show"

	DONATION_SUBSCRIBE = "oauth-donation-subscribe"
	DONATION_INDEX = "oauth-donation-index"

	CUSTOM_ALERT_STORE = "oauth-custom_alert-store"

	GOAL_SUBSCRIBE = "oauth-goal-subscribe"
	POLL_SUBSCRIBE = "oauth-poll-subscribe"

	ALL_SCOPES = [USER_SHOW, DONATION_INDEX, DONATION_SUBSCRIBE, CUSTOM_ALERT_STORE,
					GOAL_SUBSCRIBE, POLL_SUBSCRIBE]


class Channels:
	NEW_DONATION_ALERTS = "$alerts:donation_"

	DONATION_GOALS_UPDATES = "$goals:goal_"

	POLLS_UPDATES = "$polls:poll_"

	ALL_CHANNELS = [NEW_DONATION_ALERTS, DONATION_GOALS_UPDATES, POLLS_UPDATES]