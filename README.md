<p align="center">
    <a href="https://imgur.com/vfJl0Jo"><img src="https://i.imgur.com/vfJl0Jo.png" title="source: imgur.com" /></a>
    <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=30&pause=1000&color=F57D07&center=true&vCenter=true&random=false&width=435&lines=Donation;Alerts;API" alt="Typing SVG" /></a>
</p>

# О платформе DonationAlerts
**DonationAlerts** - онлайн-платформа для сбора пожертвований от зрителей в реальном времени. Часто используется стримерами и блогерами во время трансляций. Платформа предоставляет сервис для приема электронных пожертвований, уведомления о которых появляются в реальном времени. С помощью DonationAlerts создатели контента могут интегрировать различные платежные системы и настраивать персонализированные сообщения для поддерживающих.

# Об API
**API DonationAlerts** - это программный интерфейс приложения, который позволяет разработчикам взаимодействовать с функциональностью **DonationAlerts**. С его помощью можно автоматизировать процессы сбора информации о пожертвованиях, управления уведомлениями, и, возможно, другими аспектами, связанными с платформой.

> [!NOTE]
> _Для работы с **API** понадобится:_ \
> [Создать свое приложение Donation Alerts](https://www.donationalerts.com/application/clients) \
> [Официальная документация Donation Alerts API](https://www.donationalerts.com/apidoc)

> [!WARNING]
> **Новая версия модуля на стадии разработки**


## Установка
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

## Пример использования

>[!TIP]
>Если желаете работать _асинхронно_, импортируйте класс **AIODonationAlertsAPI**, методы работы аналогичны.

В данном коде реализован пример простого веб-приложения на Flask, которое обеспечивает авторизацию через DonationAlerts API и получение информации о пользователе. Давайте разберем, что происходит шаг за шагом:

#### Импорт библиотек:

```python
from flask import Flask, redirect, request
from donationalerts import DonationAlertsAPI, Scope
```
В этом блоке происходит импорт необходимых модулей. Flask используется для создания веб-приложения, а DonationAlertsAPI и Scope - для работы с DonationAlerts API и указания необходимых разрешений (scopes).

#### Настройка приложения и API:

```python
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
```
Здесь создается экземпляр Flask-приложения (app) и объекта DonationAlertsAPI с указанием идентификатора клиента (CLIENT_ID), секрета клиента (CLIENT_SECRET), URI перенаправления после авторизации (http://127.0.0.1:5000/login) и списком разрешений (scopes).

#### Маршрут для инициации авторизации:

```python
@app.route("/")
def index():
    return redirect(api.authorize.login())
```
При переходе на корневой URL приложения происходит перенаправление на URL авторизации DonationAlerts с использованием api.authorize.login().

#### Маршрут для обработки ответа после авторизации:

```python
@app.route("/login")
def login():
    code = request.args.get("code")
    access_token = api.authorize.get_access_token(code)

    user = api.user.get(access_token.access_token)
    return user.to_dict()
```
После того, как пользователь разрешил доступ, происходит перенаправление на указанный URI (http://127.0.0.1:5000/login). Затем извлекается код доступа (code), который используется для получения токена доступа. С помощью токена доступа запрашивается информация о пользователе, и возвращается словарь с данными пользователя.

#### Запуск приложения:

```python
if __name__ == "__main__":
    app.run(debug=True)
```
Приложение запускается, если оно запускается напрямую, а не импортируется в другой скрипт.

Этот код создает простое веб-приложение, которое позволяет пользователям авторизоваться через DonationAlerts, после чего выводится информация о пользователе. Важно убедиться, что идентификатор клиента и секрет клиента правильно указаны, и что URI перенаправления соответствует настройкам вашего приложения в DonationAlerts.

#### Полный код:
```python
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
