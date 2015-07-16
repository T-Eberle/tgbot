__author__ = 'Thomas'



from telegram.bot.basicapi.model.message import Message
from telegram.bot.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.bot.config.tgbotconfigparser import TGBotConfigParser
from telegram.bot.tglogging.TGLogger import logger

config = TGBotConfigParser("config.ini")
data = config.load()

class MessageController:
    def __init__(self, message:Message=None):
        self.message = message

    def sendMessage(self, chat_id, text):
        url = data.get("tgapi","bot_link") + data.get("tgapi","sendMessage_Method")
        values = {"chat_id": chat_id, "text": text}
        logger.debug("Message sent! -> "+text)
        HTTPRequestController.requestWithValues(None, url, values)
