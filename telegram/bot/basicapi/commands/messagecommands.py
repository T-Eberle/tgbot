__author__ = 'Thomas'

from telegram.bot.basicapi.model.message import Message
from telegram.bot.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.bot.config.tgbotconfigparser import TGBotConfigParser
from telegram.bot.tglogging.TGLogger import logger

config = TGBotConfigParser()
data = config.load()

class MessageController:
    def __init__(self, message:Message=None):
        self.message = message

    def sendmessage(self, chat_id, text):
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendMessage_Method")
        values = {"chat_id": chat_id, "text": text}
        logger.debug("Message sent! -> " + text)
        HTTPRequestController.requestwithvaluesxwwwurlencoded(None, url, values)

    @staticmethod
    def sendreply(message:Message,chat_id, text):
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendMessage_Method")
        values = {"chat_id": chat_id, "text": text, "reply_to_message_id": message.message_id}
        logger.debug("Reply sent! -> " + text)
        HTTPRequestController.requestwithvaluesxwwwurlencoded(None, url, values)
