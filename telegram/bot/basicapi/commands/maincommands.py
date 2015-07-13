__author__ = 'Tommy'

import sys

from weareone.common.weAreOneParameters import bot_link, \
    getUpdates_Method
from telegram.bot.basicapi import HTTPRequestController


class MainController:
    def setWebHook(self, external_url):
        url = bot_link + getUpdates_Method
        values = {'url': external_url}
        print(HTTPRequestController.requestWithValues(None, url, values))

    def getNewestUpdate(self, update_id=sys.maxsize):
        url = bot_link + getUpdates_Method
        values = {'offset': update_id}
        print(HTTPRequestController.requestWithValues(None, url, values))

    def getUpdates(self):
        url = bot_link + getUpdates_Method
        values = {'offset': sys.maxsize}
        print(HTTPRequestController.requestWithValues(None, url, values))
