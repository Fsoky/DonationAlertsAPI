class Scopes:
	"""Обозначения

	USER_SHOW: получения данных профиля

	DONATION_SUBSCRIBE: подписка на новые уведомления о пожертвованиях
	DONATION_INDEX: просмотр пожертвований

	CUSTOM_ALERT_STORE: создание пользовательских предупреждений

	GOAL_SUBSCRIBE: подписка на обновления целей пожертвований
	POLL_SUBSCRIBE: подписка на обновления опросов

	ALL_SCOPES: все права в одном списке

	"""

	USER_SHOW = "oauth-user-show"

	DONATION_SUBSCRIBE = "oauth-donation-subscribe"
	DONATION_INDEX = "oauth-donation-index"

	CUSTOM_ALERT_STORE = "oauth-custom_alert-store"

	GOAL_SUBSCRIBE = "oauth-goal-subscribe"
	POLL_SUBSCRIBE = "oauth-poll-subscribe"

	ALL_SCOPES = [USER_SHOW, DONATION_INDEX, DONATION_SUBSCRIBE, CUSTOM_ALERT_STORE,
					GOAL_SUBSCRIBE, POLL_SUBSCRIBE]


class Channels:
	"""Обозначения

	NEW_DONATION_ALERTS: новые оповещания о пожертвованиях

	DONATION_GOALS_UPDATES: обновления целей пожертвования

	POLLS_UPDATES: обновления опросов

	ALL_CHANNELS: все каналы в одном списке

	"""

	NEW_DONATION_ALERTS = "$alerts:donation_"

	DONATION_GOALS_UPDATES = "$goals:goal_"

	POLLS_UPDATES = "$polls:poll_"

	ALL_CHANNELS = [NEW_DONATION_ALERTS, DONATION_GOALS_UPDATES, POLLS_UPDATES]