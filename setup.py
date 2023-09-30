from setuptools import setup, find_packages
from io import open


def read(filename):
   with open(filename, "r", encoding="utf-8") as file:
      return file.read()


setup(name="DonationAlertsAPI",
   version="2.1",
   description="Module for simple work with API Donation Alerts",
   long_description=read("README.md"),
   long_description_content_type="text/markdown",
   author="Fsoky",
   author_email="cyberuest0x12@gmail.com",
   url="https://github.com/Fsoky/DonationAlertsAPI",
   keywords="api donation donationalerts python",
   packages=find_packages()
)