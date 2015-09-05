# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.basicapi.model.message import Message
from telegram.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger

config = TGBotConfigParser("config.ini")
data = config.load()


class MessageController:
    def __init__(self, message: Message=None):
        self.message = message

    @staticmethod
    def sendmessage(chat_id, text):
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendMessage_Method")
        values = {"chat_id": chat_id, "text": text}
        logger.debug("Message sent! -> " + text)
        HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values)

    @staticmethod
    def sendreply(message: Message, chat_id, text):
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendMessage_Method")
        values = {"chat_id": chat_id, "text": text, "reply_to_message_id": message.message_id}
        logger.debug("Reply sent! -> " + text)
        HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values)
