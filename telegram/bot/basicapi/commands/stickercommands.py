__author__ = 'Thomas'

from telegram.bot.basicapi.model.sticker import Sticker
from telegram.bot.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.bot.config.tgbotconfigparser import TGBotConfigParser
from telegram.bot.tglogging.TGLogger import logger

config = TGBotConfigParser()
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
