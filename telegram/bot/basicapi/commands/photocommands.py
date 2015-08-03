__author__ = 'Thomas Eberle'

from telegram.bot.config.tgbotconfigparser import TGBotConfigParser
from telegram.bot.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.bot.tglogging.TGLogger import logger

config = TGBotConfigParser("config.ini")
data = config.load()


class PhotoController:
    def __init__(self, photo=None):
        self.photo = photo

    def sendphoto(self, chat_id, photo):
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendPhoto_Method")
        values = {"chat_id": chat_id, "photo": photo}
        logger.debug("Photo sent! -> " + photo)
        HTTPRequestController.requestwithvaluesmultipart(None, url, values)
