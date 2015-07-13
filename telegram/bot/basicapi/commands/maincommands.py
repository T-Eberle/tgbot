__author__ = 'Tommy'

import sys

from weareone.common.weAreOneParameters import bot_link, \
    getUpdates_Method
from telegram.bot.basicapi import HTTPRequestController
from telegram.bot.config.tgbotconfigparser import TGBotConfigParser

data = TGBotConfigParser("config.ini").config


class MainController:
    def setWebHook(self, external_url):
        url = data.get("tgapi","bot_link") + data.get("tgapi","setWebhook_Method")
        values = {'url': external_url}
        print(HTTPRequestController.requestWithValues(None, url, values))

    def getNewestUpdate(self, update_id=sys.maxsize):
        url = data.get("tgapi","bot_link") + data.get("tgapi","getUpdates_Method")
        values = {'offset': update_id}
        print(HTTPRequestController.requestWithValues(None, url, values))

    def getUpdates(self):
        url = data.get("tgapi","bot_link") + data.get("tgapi","getUpdates_Method")
        values = {'offset': sys.maxsize}
        print(HTTPRequestController.requestWithValues(None, url, values))
