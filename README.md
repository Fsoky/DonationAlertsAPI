[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=F79913&center=true&vCenter=true&width=435&lines=Donation+Alerts+API;Work+with+donations)](https://git.io/typing-svg)

# [!] Модуль в разработке.

#### 🛠 Инструменты
![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![aiohttp](https://img.shields.io/badge/aiohttp-green?style=for-the-badge&logo=aiohttp)
![requests](https://img.shields.io/badge/requests-important?style=for-the-badge)
![asyncio](https://img.shields.io/badge/asyncio-red?style=for-the-badge)
![json](https://img.shields.io/badge/json-gray?style=for-the-badge&logo=json)
![datetime](https://img.shields.io/badge/datetime-blueviolet?style=for-the-badge)

## Установка 💾
- Установка, используя пакетный менеджер pip
```
$ pip install DonationAlertsAPI
```
- Установка с GitHub *(требуется [git](https://git-scm.com/downloads))*
```
$ git clone https://github.com/Fsoky/DonationAlertsAPI
$ cd DonationAlertsAPI
$ python setup.py install
```
- Или
```
$ pip install git+https://github.com/Fsoky/DonationAlertsAPI
```

## Дополнительно
Создайте свое собственное приложение для работы с *DA API*

[Создать свое приложение Donation Alerts](https://www.donationalerts.com/application/clients) \
[Официальная документация Donation Alerts API](https://www.donationalerts.com/apidoc)

## Пример использования
```py
from flask import Flask, redirect, request
from donationalerts import DonationAlertsAPI, Scope

app = Flask(__name__)
api = DonationAlertsAPI(
    "CLIENT_ID",
    "CLIENT_SECRET",
    "http://127.0.0.1:5000/login",
    [
        Scope.OAUTH_USER_SHOW,
        Scope.OAUTH_DONATION_INDEX
    ]
)


@app.get("/")
def index():
    return redirect(api.authorize.login())


@app.get("/login")
def login():
    code = request.args.get("code")
    access_token = api.authorize.get_access_token(code)

    user = api.user.get(access_token.access_token)
    return user.to_dict()


if __name__ == "__main__":
    app.run(debug=True)
```

> Если желаете работать _асинхронно_, импортируйте класс **AIODonationAlertsAPI**, методы работы аналогичны.
