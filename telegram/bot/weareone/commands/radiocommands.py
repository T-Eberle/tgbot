__author__ = 'Thomas'

from telegram.bot.basicapi.commands.messagecommands import MessageController
from telegram.bot.basicapi.commands.stickercommands import StickerController
from telegram.bot.tglogging.TGLogger import logger
from telegram.bot.config.tgbotfileidparser import TGBotFileIDParser
from telegram.bot.config.weareonejsonparser import WeAreOneJSONParser
from telegram.bot.weareone.commands.commandutilities import getparameter

bradiocommands = ["listener", "dj", "now", "track","sendeplan"]

radiostreams = ["technobase","housetime","hardbase","trancebase","coretime","clubtime"]

allradiocommands = bradiocommands+radiostreams
waoParser = WeAreOneJSONParser("housetime_onAir")

config = TGBotFileIDParser()
data = config.load()


class RadioCommands:

    def parseradiocommands(self,message, text):
        logger.debug(text + " command recognized.")
        for bradiocommand in bradiocommands:
            if (bradiocommand in text):
                self.basicradiocommand(message,text,bradiocommand)
        for radiostream in radiostreams:
           if("/"+radiostream == text):
            StickerController.sendstickerwithid(message.chat_id(), data.get("file_ids", radiostream))

    def track(self,message,stream):
        artist = waoParser.getjsonelement(stream+"_onAir","artist")
        track = waoParser.getjsonelement(stream+"_onAir","track")
        MessageController.sendreply(message, message.chat_id(),
                                    "\U0001F3B6" + "Aktueller Track @ "+stream.capitalize()+ ": " + artist + " - " +track+ "\n #track")


    @staticmethod
    def sendeplan(message):
        MessageController.sendreply(message, message.chat_id(),
                                    "Der Sendeplan ist leer.... \n" +
                                    "Ich bin enttaeuscht!#sendeplan")
    @staticmethod
    def dj(message, stream):
        dj = waoParser.getjsonelement(stream + "_onAir", "dj")
        if dj:
            MessageController.sendreply(message, message.chat_id(),
                                        "\U0001F3A4" + "Aktueller DJ @ " + stream.capitalize() + ": " + dj + "\n #dj")
        else:
            MessageController.sendreply(message, message.chat_id(),
                                        "\U0001F44EKein DJ ON AIR @ " + stream.capitalize() + "!\n #dj")
    @staticmethod
    def listener(message, stream):
        listener = waoParser.getjsonelement(stream + "_onAir", "listener")
        MessageController.sendreply(message, message.chat_id(),
                                    "\U0001F4E1" + "Aktuelle Listeneranzahl @ " + stream.capitalize() + ": " + listener + "\n #listener")
    @staticmethod
    def now(message, stream):
        dj = waoParser.getjsonelement(stream + "_onAir", "dj")
        show = waoParser.getjsonelement(stream + "_onAir", "show")
        style = waoParser.getjsonelement(stream + "_onAir", "style")
        start = waoParser.getjsonelement(stream + "_onAir", "start")
        end = waoParser.getjsonelement(stream + "_onAir", "end")
        if dj:
            MessageController.sendreply(message, message.chat_id(),
                                        "\U00002139Aktuelle Show-Info @ " + stream.capitalize() + "\U00002139\n" +
                                        "\U0001F3A4" + "DJ: " + dj + "\n" +
                                        "\U0001F4E2" + "Showname: " + show + "\n" +
                                        "\U0001F3A7" + "Style: " + style + "\n" +
                                        "\U000023F0Uhrzeit: " + start + ":00 bis " + end + ":00\n #now")
        else:
            MessageController.sendreply(message, message.chat_id(),
                                        "\U0001F44EKein DJ ON AIR @ " + stream.capitalize() + "!\n #now")

    def basicradiocommand(self,message,text,method_name):
        parameter = getparameter(text).lower()
        if "all" in parameter:
            for stream in radiostreams:
                getattr(self,method_name)(message,stream)
        elif not any(radio in parameter for radio in radiostreams):
            MessageController.sendreply(message, message.chat_id(),
                                        "\U0000274CBitte den Radiostream als Parameter mitgeben!\n #"+method_name)
        else:
            for radiostream in radiostreams:
                if radiostream in parameter:
                    getattr(self,method_name)(message,radiostream)


