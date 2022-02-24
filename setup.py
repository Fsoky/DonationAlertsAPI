from setuptools import setup, find_packages
from io import open
import re


def read(filename):
	with open(filename, encoding="utf-8") as file:
		return file.read()


with open("donationalerts/version.py", "r", encoding="utf-8") as file:
	version = re.findall(r"[0-9]+.[0-9]+.[0-9]+", file.read())[0]

setup(name="DonationAlertsAPI",
	version=version,
	description="Модуль для работы с Donation Alerts API",
	long_description=read("README.md"),
	long_description_content_type="text/markdown",
	packages=find_packages(),
	author="Fsoky Community",
	author_email="cyberuest0x12@gmail.com",
	url="https://github.com/Fsoky/DonationAlertsAPI",
	keywords="donationalerts api tools",
	install_requires=[
		"aiohttp",
		"python_socketio",
		"requests",
		"websocket_client",
		"websockets"
	]
)