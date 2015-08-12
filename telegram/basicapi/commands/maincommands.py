# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import sys

from telegram.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.config.tgbotconfigparser import TGBotConfigParser

data = TGBotConfigParser("config.ini").config


class MainController:
    def setWebHook(self, external_url):
        url = data.get("tgapi","bot_link") + data.get("tgapi","setWebhook_Method")
        values = {'url': external_url}
        print(HTTPRequestController.requestwithvaluesxwwwurlencoded(None, url, values))

    def getNewestUpdate(self, update_id=sys.maxsize):
        url = data.get("tgapi","bot_link") + data.get("tgapi","getUpdates_Method")
        values = {'offset': update_id}
        print(HTTPRequestController.requestwithvaluesxwwwurlencoded(None, url, values))

    def getUpdates(self):
        url = data.get("tgapi","bot_link") + data.get("tgapi","getUpdates_Method")
        values = {'offset': sys.maxsize}
        print(HTTPRequestController.requestwithvaluesxwwwurlencoded(None, url, values))
