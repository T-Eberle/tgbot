from distutils.core import setup

setup(name="TGBot",
      version="0.9",
      description="Framework to build a Telegram Bot with uwsgi functions",
      author= "Thomas Eberle",
      author_email="Thomas@tommyelroy.com",
      url="https://github.com/T-Eberle/tgbot",
      keywords = "telegram bot",
      packages = ["resources","resources.config","telegram","telegram.basicapi","telegram.basicapi.commands",
                  "telegram.basicapi.decorator","telegram.basicapi.http","telegram.basicapi.model",
                  "telegram.basicapi.wsgi",
                  "telegram.config","telegram.tglogging","telegram.tgredis"]
      )