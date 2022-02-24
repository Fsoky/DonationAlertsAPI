![DA API](https://github.com/Fsoky/Donation-Alerts-API-Python/blob/main/images/dapi_banner.jpg)

## Инструменты 🛠
![Python](https://img.shields.io/badge/Python-3.8-blue?style=for-the-badge&logo=python)
![aiohttp](https://img.shields.io/badge/aiohttp-3.8.1-blue?style=for-the-badge&logo=aiohttp)
![python-socketio](https://img.shields.io/badge/socketio-5.5.2-blue?style=for-the-badge)
![websockets](https://img.shields.io/badge/websockets-10.2-blue?style=for-the-badge)
![websocket-client](https://img.shields.io/badge/websocket_client-1.2.3-blue?style=for-the-badge)

![requests](https://img.shields.io/badge/requests-important?style=for-the-badge)
![asyncio](https://img.shields.io/badge/asyncio-red?style=for-the-badge)
![json](https://img.shields.io/badge/json-green?style=for-the-badge&logo=json)
![datetime](https://img.shields.io/badge/datetime-blueviolet?style=for-the-badge)

## Установка 💾
`windows:` pip install DonationAlertsAPI

`linux` `macos:` pip3 install DonationAlertsAPI

- **Дополнительно** \
[Создать свое приложение Donation Alerts](https://www.donationalerts.com/application/clients) \
[Официальная документация Donation Alerts API](https://www.donationalerts.com/apidoc)

## Пример использования 🎈
```py
from flask import Flask, redirect, request
from donationalerts import DonationAlertsAPI, Scopes

app = Flask(__name__)
api = DonationAlertsAPI("client id", "client secret", "http://127.0.0.1:5000/login", Scopes.USER_SHOW)

@app.route("/", methods=["GET"])
def index():
    return redirect(api.login())


@app.route("/login", methods=["GET"])
def login():
    code = request.args.get("code")
    access_token = api.get_access_token(code)
    
    user = api.user(access_token)
    return user.objects


if __name__ == "__main__":
    app.run(debug=True)
```

*[Смотреть больше примеров](https://github.com/Fsoky/Donation-Alerts-API-Python/tree/main/examples)*

**Обзоры версий 👀** \
[Donation Alerts API Версия 1.0.0](https://www.youtube.com/watch?v=ZJVVDRNR9Vw) \
[Donation Alerts API Версия 1.0.6](https://www.youtube.com/watch?v=pAdPuScKSNs) \
[Donation Alerts API Версия 2.0.0](https://www.youtube.com/watch?v=ln7fvwdy5zo)

### Присоединяйся к нам
[![Vkontakte](https://img.shields.io/badge/Vkontakte-black?style=for-the-badge&logo=VK)](https://vk.com/fsoky)
[![YouTube](https://img.shields.io/badge/YouTube-red?style=for-the-badge&logo=YouTube)](https://youtube.com/c/Фсоки)
[![Telegram](https://img.shields.io/badge/Telegram-blue?style=for-the-badge&logo=Telegram)](https://t.me/fsokycommunity)
