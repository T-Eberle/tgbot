__author__ = 'Thomas'

from telegram.bot.tgconfigparser.tgbotconfigparser import TGBotConfigParser

config = TGBotConfigParser("server.ini")
data = config.load()

address = data.get("basics","address")

port = int(data.get("basics","port"))

keyfile = data.get("ssl","keyfile")

certfile = data.get("ssl","certfile")

ca_certs = data.get("ssl","ca_certs")
