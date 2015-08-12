# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.basicapi.model.sticker import Sticker
from telegram.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger

config = TGBotConfigParser("config.ini")
data = config.load()


class StickerController:
    def __init__(self, sticker:Sticker=None):
        self.sticker = sticker

    @staticmethod
    def sendstickerwithid(chat_id, file_id):
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendSticker_Method")
        values = {"chat_id": chat_id, "sticker": file_id}
        logger.debug("Sticker sent! -> ID #" + file_id)
        HTTPRequestController.requestwithvaluesxwwwurlencoded(None, url, values)
