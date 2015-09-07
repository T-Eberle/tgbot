# -*- coding: utf-8 -*-
__author__ = 'Thomas'

import urllib.request
import json
import html
import requests
from datetime import datetime, timedelta
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger

config = TGBotConfigParser("wao-config.ini").config
timeformat = "%H:%M"


class WAOAPIParser:
    def __init__(self, tray=None,waoapi=None):
        self.tray = tray
        self.waoapi=waoapi
        self.data = None
        self.showplan= None
        self.url = None
        if self.tray:
            self.loadtray(tray)

    @staticmethod
    def getjson(url,values=None):
        result = requests.get(url,params=values)
        return result.json()

    @staticmethod
    def method(method):
        url = config.get("waoapi", "url")
        return WAOAPIParser.getjson(url+method)

    @staticmethod
    def radiostation(stream):
        radio = WAOAPIParser.method(config.get("waoapi", "radio"))
        stream_key =config.get("waoapi-radio", stream)
        return radio[stream_key]

    @staticmethod
    def tracklist(stream):
        pass

    @staticmethod
    def now(stream, value):
        radiostation = WAOAPIParser.radiostation(stream)
        return radiostation[config.get("waoapi-station", value)]

    @staticmethod
    def nowartist(stream):
        return WAOAPIParser.now(stream,"trackartist")

    @staticmethod
    def nowtrack(stream):
        return WAOAPIParser.now(stream,"tracktitle")

    @staticmethod
    def nowrelease(stream):
        return WAOAPIParser.now(stream,"releaseid")

    @staticmethod
    def correcdate(timestamp):
        timestamp = str(timestamp)[:-3]
        return datetime.fromtimestamp(int(timestamp))

    @staticmethod
    def correctdate_timeformat(timestamp,format=None):
        if format:
            result_timeformat = format
        else:
            result_timeformat = timeformat
        return WAOAPIParser.correcdate(timestamp).strftime(result_timeformat)

    @staticmethod
    def nowstart(stream):
        start = str(WAOAPIParser.now(stream, "start"))
        start_date = WAOAPIParser.correcdate(int(start))
        return start_date

    @staticmethod
    def nowstart_string(stream):
        return WAOAPIParser.nowstart(stream).strftime(timeformat)

    @staticmethod
    def nowend(stream):
        end = str(WAOAPIParser.now(stream, "end"))
        end_date = WAOAPIParser.correcdate(end)
        return end_date

    @staticmethod
    def nowend_string(stream):
        return WAOAPIParser.nowend(stream).strftime(timeformat)

    def loadtray(self, tray):
        self.tray = tray
        url = config.get("weareone", "tray") + config.get("weareone", self.tray)
        response = urllib.request.urlopen(url)
        self.data = json.loads(response.read().decode("utf-8"))
        return self.data

    def loadwaoapishowplan(self, waoapi=None,count=-1,upcoming=False,site=1):
        if not self.waoapi and not waoapi:
            logger.error("You need to set the variable waoapi.")
            return
        elif not self.waoapi and waoapi:
            self.waoapi = waoapi
        url = config.get("waoapi", "url") + config.get("waoapi", "showplan")+config.get("waoapi-site",self.waoapi)\
              +"/"+str(site)
        logger.info(url)
        values = {"count":count,"upcoming":upcoming}
        self.showplan = WAOAPIParser.getjson(url,values)
        return self.showplan

    def gettrayelement(self, json_file, jsonid):
        data = self.loadtray(json_file)
        return html.unescape(data[jsonid])


if __name__ == '__main__':
    waoconfig = TGBotConfigParser("wao-config.ini")
    waodata =waoconfig.load()
    waoapi = WAOAPIParser(waoapi="housetime")
    waoapi.loadwaoapishowplan(count=2)
    print(str(waoapi.showplan))
    waoapi = WAOAPIParser(waoapi="housetime")
    two_shows = waoapi.loadwaoapishowplan(count=2,upcoming=True)
    for show in two_shows:
        start_timestamp= show[waodata.get("waoapi-showplan","start")]
        start_date = WAOAPIParser.correcdate(start_timestamp)
        print(str(start_date))

