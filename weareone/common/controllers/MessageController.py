__author__ = 'Thomas'

import weareone.common.weAreOneParameters
from weareone.common.types.message import Message
from urllib.request import Request, urlopen
from urllib import parse
from weareone.common.weAreOneParameters import bot_link, \
    getMe_Method, sendMessage_Method, getUpdates_Method, setWebhook_Method


class MessageController:
    def __init__(self, message:Message=None):
        self.message = message

    def getme(self):
        response = urlopen(bot_link + getMe_Method)
        html = response.read()

        print(html)

    def getmessage(self):
        response = urlopen(bot_link + sendMessage_Method)
        html = response.read()

        print(html)

    def setWebHook(self):
        print(bot_link + setWebhook_Method)

        response = urlopen(bot_link + setWebhook_Method)
        #TODO POST with values from getUpdates Method!
        # values = {'url': None}
        #
        # data = urlencode(values)
        # binary_data = data.encode("utf-8")
        # req = Request(response, binary_data)
        html = response.read()

        print(html)

    def getupdates(self):
        #TODO POST with values from getUpdates Method!
        response = urlopen(bot_link + getUpdates_Method)
        html = response.read()

        print(html)
