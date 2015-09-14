# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger

config = TGBotConfigParser("config.ini")
data = config.load()


class PhotoController:
    def __init__(self, photo=None):
        self.photo = photo

    @staticmethod
    def sendphoto(chat_id, photo):
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendPhoto_Method")
        values = {"chat_id": chat_id, "photo": photo}
        logger.debug("Photo sent! -> " + photo)
        pass
