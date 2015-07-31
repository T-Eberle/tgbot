__author__ = 'Thomas'

from telegram.bot.basicapi.commands.messagecommands import MessageController
from telegram.bot.basicapi.commands.stickercommands import StickerController
from telegram.bot.tglogging.TGLogger import logger
from telegram.bot.config.tgbotfileidparser import TGBotFileIDParser
from telegram.bot.config.weareonejsonparser import WeAreOneJSONParser
from telegram.bot.weareone.commands.commandutilities import *

bradiocommands = ["listener", "dj", "now", "track", "heute","next","montag","dienstag","mittwoch","donnerstag","freitag","samstag","sonntag"]

radiostreams = {"tb": "technobase", "ht": "housetime", "hb": "hardbase", "trb": "trancebase", "crt": "coretime",
                "clt": "clubtime"}


allradiocommands = bradiocommands + list(radiostreams.values())
waoParser = WeAreOneJSONParser("housetime_onAir")

config = TGBotFileIDParser()
data = config.load()


class RadioCommands:
    def parseradiocommands(self, message, text):
        self.chat={message.chat_id():"housetime"}
        logger.debug(text + " command recognized.")
        for bradiocommand in bradiocommands:
            if getcommand(text)==bradiocommand:
                    self.basicradiocommand(message, text, bradiocommand)
        for radiostream in list(radiostreams.values()):
            if radiostream == getcommand(text):
                StickerController.sendstickerwithid(message.chat_id(), data.get("file_ids", radiostream))

    def basicradiocommand(self, message, text, method_name):
        try:
            parameter = getparameter(text,self.chat.get(message.chat_id()))
            reply=""
            logger.debug("PARAMETER: "+parameter)
            if "wao" in parameter or "all" in parameter:
                for stream in radiostreams.values():
                    reply += getattr(self, method_name)(message, stream)
                MessageController.sendreply(message, message.chat_id(), reply + " #" + method_name)
            elif not (any(radio in parameter for radio in list(radiostreams.values())) or any(
                            radio in parameter for radio in list(radiostreams.keys()))):
                MessageController.sendreply(message, message.chat_id(),
                                            "\U0000274CBitte den Radiostream als Parameter mitgeben!\n #" + method_name)
            else:
                for radiostream in radiostreams.items():
                    if radiostream[0] in parameter or radiostream[1] in parameter:
                        reply += getattr(self, method_name)(message, radiostream[1])
                MessageController.sendreply(message, message.chat_id(), reply)
        except TypeError as typo:
            MessageController.sendreply(message, message.chat_id(), "Witzbold.")
            logger.info(typo)

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
    def next(message,stream):
        showplan = waoParser.load(stream+"_shows")
        return nextshow(showplan,stream)

    @staticmethod
    def track(message, stream):
        artist = waoParser.getjsonelement(stream + "_onAir", "artist")
        track = waoParser.getjsonelement(stream + "_onAir", "track")
        return str("\U0001F3B6" + "Aktueller Track @ " + stream.capitalize() + ": " + artist + " - " + track + "\n")


    @staticmethod
    def dj(message, stream):
        dj = waoParser.getjsonelement(stream + "_onAir", "dj")
        if dj:
            return str("\U0001F3A4" + "Aktueller DJ @ " + stream.capitalize() + ": " + dj + "\n")
        else:
            return str("\U0001F44EKein DJ ON AIR @ " + stream.capitalize() + "!\n")

    @staticmethod
    def listener(message, stream):
        listener = waoParser.getjsonelement(stream + "_onAir", "listener")
        return str("\U0001F4E1" + "Aktuelle Listeneranzahl @ " + stream.capitalize() + ": " + listener + "\n")

    @staticmethod
    def now(message, stream):
        dj = waoParser.getjsonelement(stream + "_onAir", "dj")
        show = waoParser.getjsonelement(stream + "_onAir", "show")
        style = waoParser.getjsonelement(stream + "_onAir", "style")
        start = waoParser.getjsonelement(stream + "_onAir", "start")
        end = waoParser.getjsonelement(stream + "_onAir", "end")
        if dj:
            return str("\U00002139Aktuelle Show-Info @ " + stream.capitalize() + "\U00002139\n"
                       + "\U0001F3A4" + "DJ: " + dj + "\n" + "\U0001F4E2"
                       + "Showname: " + show + "\n" + "\U0001F3A7" +
                       "Style: " + style + "\n" + "\U000023F0Uhrzeit: "
                       + start + ":00 bis " + end + ":00\n")

        else:
            return str("\U00002139Aktuelle Show-Info @ " + stream.capitalize() + "\U00002139\n" +
                       "\U0001F44EKein DJ ON AIR @ " + stream.capitalize() + "!\n")

