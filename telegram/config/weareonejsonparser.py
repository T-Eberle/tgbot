# -*- coding: utf-8 -*-
__author__ = 'Thomas'

import urllib.request
import json
import html

from telegram.config.tgbotconfigparser import TGBotConfigParser

config = TGBotConfigParser("wao-config.ini").config


class WeAreOneJSONParser:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = None
        self.load(json_file)

    def load(self, json_file):
        self.json_file = json_file
        url = config.get("weareone", "tray") + config.get("weareone", self.json_file)
        response = urllib.request.urlopen(url)
        self.data = json.loads(response.read().decode("utf-8"))
        return self.data

    def getjsonelement(self, json_file, jsonid):
        data = self.load(json_file)
        return html.unescape(data[jsonid])


if __name__ == '__main__':
    waoParser = WeAreOneJSONParser("housetime_onAir")
    print(waoParser.getjsonelement("housetime_onAir", "listener"))
