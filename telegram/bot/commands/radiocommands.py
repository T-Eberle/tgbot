# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.basicapi.commands.messagecommands import MessageController
from telegram.basicapi.commands.stickercommands import StickerController
from telegram.tglogging import logger
from telegram.bot.commands import *
from telegram.config.tgbotfileidparser import TGBotFileIDParser
from telegram.config.weareonejsonparser import WeAreOneJSONParser
from telegram.config.jsonconfigreader import JSONConfigReader
from telegram.tgredis import *
import collections

multipleradiocommands = ["listener", "dj", "now", "track", "next"]

singleradiocommands = ["heute","morgen","montag","dienstag","mittwoch","donnerstag","freitag","samstag","sonntag"]

unsorted_radiostreams = {"tb": "technobase", "ht": "housetime", "hb": "hardbase", "trb": "trancebase", "ct": "coretime",
                "clt": "clubtime"}
radiostreams = collections.OrderedDict(sorted(unsorted_radiostreams.items()))


allradiocommands = multipleradiocommands + singleradiocommands + list(radiostreams.values())
waoParser = WeAreOneJSONParser("housetime_onAir")

fileconfig = TGBotFileIDParser()
filedata = fileconfig.load()

class RadioCommands:
    def parseradiocommands(self, message, text):
        user = message.from_User
        jsonuser.read()
        jsongroup.read()
        self.chat = getStreamParameter(message)
        logger.debug(text + " command recognized.")
        for multipleradiocommand in multipleradiocommands:
            if getcommand(text)== multipleradiocommand:
                    self.basicradiocommand(message, text, multipleradiocommand,False)
        for singleradiocommand in singleradiocommands:
            if getcommand(text)== singleradiocommand:
                    self.basicradiocommand(message, text, singleradiocommand,True)
        for radiostream in list(radiostreams.values()):
            if radiostream == getcommand(text):
                StickerController.sendstickerwithid(message.chat_id(), filedata.get("file_ids", radiostream))

    def basicradiocommand(self, message, text, method_name,multiple_message):
        try:
            parameter = getparameter(text,self.chat)
            reply=""
            if "wao" in parameter or "all" in parameter:
                if multiple_message:
                    for stream in radiostreams.values():
                        reply = getattr(self, method_name)(message, stream)
                        MessageController.sendreply(message, message.chat_id(), reply+"#%s"%(method_name))
                else:
                    for stream in radiostreams.values():
                        reply += getattr(self, method_name)(message, stream)
                    MessageController.sendreply(message, message.chat_id(), reply+"#%s"%(method_name))
            elif not (any(radio in parameter for radio in list(radiostreams.values())) or any(
                            radio in parameter for radio in list(radiostreams.keys()))):
                MessageController.sendreply(message, message.chat_id(),
                                            "\U0000274CBitte den Radiostream als Parameter mitgeben!\n#" + method_name)
            else:
                if multiple_message:
                    for radiostream in radiostreams.items():
                        if radiostream[0] in parameter or radiostream[1] in parameter:
                            reply = getattr(self, method_name)(message, radiostream[1])
                            MessageController.sendreply(message, message.chat_id(), reply+"#%s"%(method_name))
                else:
                    for radiostream in radiostreams.items():
                        if radiostream[0] in parameter or radiostream[1] in parameter:
                            reply += getattr(self, method_name)(message, radiostream[1])
                    MessageController.sendreply(message, message.chat_id(), reply+"#%s"%(method_name))
        except TypeError as typo:
            logger.exception(typo)
            MessageController.sendreply(message, message.chat_id(), "Witzbold.")

    @staticmethod
    def montag(message,stream):
        showplan = waoParser.load(stream+"_shows")
        return getshowfromday(showplan,0,stream)

    @staticmethod
    def dienstag(message,stream):
        showplan = waoParser.load(stream+"_shows")
        return getshowfromday(showplan,1,stream)

    @staticmethod
    def mittwoch(message,stream):
        showplan = waoParser.load(stream+"_shows")
        return getshowfromday(showplan,2,stream)

    @staticmethod
    def donnerstag(message,stream):
        showplan = waoParser.load(stream+"_shows")
        return getshowfromday(showplan,3,stream)

    @staticmethod
    def freitag(message,stream):
        showplan = waoParser.load(stream+"_shows")
        return getshowfromday(showplan,4,stream)

    @staticmethod
    def samstag(message,stream):
        showplan = waoParser.load(stream+"_shows")
        return getshowfromday(showplan,5,stream)

    @staticmethod
    def sonntag(message,stream):
        showplan = waoParser.load(stream+"_shows")
        return getshowfromday(showplan,6,stream)

    @staticmethod
    def heute(message,stream):
        showplan = waoParser.load(stream+"_shows")
        return getshowfromtoday(showplan,stream)

    @staticmethod
    def morgen(message,stream):
        showplan = waoParser.load(stream+"_shows")
        return getshowfromtomorrow(showplan,stream)

    @staticmethod
    def next(message,stream):
        showplan = waoParser.load(stream+"_shows")
        return nextshow(showplan,stream)

    @staticmethod
    def track(message, stream):
        artist = waoParser.getjsonelement(stream + "_onAir", "artist")
        track = waoParser.getjsonelement(stream + "_onAir", "track")
        return str('''\U0001F3B6Aktueller Track @ %s: %s - %s
'''% (stream.capitalize(),artist,track))


    @staticmethod
    def dj(message, stream):
        jsonuser.read()
        jsonfile = jsonuser.jsondata
        dj = waoParser.getjsonelement(stream + "_onAir", "dj")
        id = waoParser.getjsonelement(stream + "_onAir","djid")
        if dj:
            return str('''\U0001F3A4Aktueller DJ @ %s: %s
'''% (stream.capitalize(),getDJNameByOnAir(dj,id,jsonfile)))
        else:
            return str('''\U0001F44EKein DJ ON AIR @ %s!
'''%(stream.capitalize()))

    @staticmethod
    def listener(message, stream):
        listener = waoParser.getjsonelement(stream + "_onAir", "listener")
        return str('''\U0001F4E1Aktuelle Listeneranzahl @ %s: %s
'''%(stream.capitalize(),listener))

    @staticmethod
    def now(message, stream):
        jsonuser.read()
        jsonfile = jsonuser.jsondata
        dj = waoParser.getjsonelement(stream + "_onAir", "dj")
        id = waoParser.getjsonelement(stream + "_onAir","djid")
        show = waoParser.getjsonelement(stream + "_onAir", "show")
        style = waoParser.getjsonelement(stream + "_onAir", "style")
        start = waoParser.getjsonelement(stream + "_onAir", "start")
        end = waoParser.getjsonelement(stream + "_onAir", "end")
        if dj:
            return str('''\U00002139Aktuelle Show-Info @ %s\U00002139
\U0001F3A4DJ: %s
\U0001F4E2Showname: %s
\U0001F3A7Style: %s
\U000023F0Uhrzeit: %s:00 bis %s:00
'''%(stream.capitalize(),getDJNameByOnAir(dj,id,jsonfile),show,style,start,end))

        else:
            return str('''\U00002139Aktuelle Show-Info @ %s\U00002139
\U0001F44EKein DJ ON AIR!
'''%(stream.capitalize()))

