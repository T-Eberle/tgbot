# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import sys

from telegram.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.config.tgbotconfigparser import TGBotConfigParser

data = TGBotConfigParser("config.ini").config


class MainController:
    @staticmethod
    def setwebhook(external_url):
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "setWebhook_Method")
        values = {'url': external_url}
        print(HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values))

    @staticmethod
    def getnewestupdate(update_id=sys.maxsize):
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "getUpdates_Method")
        values = {'offset': update_id}
        print(HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values))

    @staticmethod
    def getupdates():
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "getUpdates_Method")
        values = {'offset': sys.maxsize}
        print(HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values))
