# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import collections

from telegram.basicapi.commands.stickercommands import StickerController
from telegram.bot.commands import *
from telegram.config.tgbotfileidparser import TGBotFileIDParser
from telegram.config.weareonejsonparser import WeAreOneJSONParser
from telegram.tgredis import *
from resources import emoji

multipleradiocommands = ["listener", "dj", "now", "track", "next"]

singleradiocommands = ["heute", "morgen", "montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag",
                       "sonntag"]

unsorted_radiostreams = {"tb": "technobase", "ht": "housetime", "hb": "hardbase", "trb": "trancebase", "ct": "coretime",
                         "clt": "clubtime"}
radiostreams = collections.OrderedDict(sorted(unsorted_radiostreams.items()))

allradiocommands = multipleradiocommands + singleradiocommands + list(radiostreams.values())
waoParser = WeAreOneJSONParser("housetime_onAir")

fileconfig = TGBotFileIDParser()
filedata = fileconfig.load()


class RadioCommands:
    def __init__(self):
        self.chat = None

    def parseradiocommands(self, message, text):
        """
        Parser für Radiocommands
        :param message: Die vom Nutzer verschickte Nachricht
        :param text: Der vom Nutzer verschickte Text
        """
        self.chat = getstreamparameter(message)
        logger.debug(text + " command recognized.")
        for multipleradiocommand in multipleradiocommands:
            if getcommand(text) == multipleradiocommand:
                self.basicradiocommand(message, text, multipleradiocommand, False)
        for singleradiocommand in singleradiocommands:
            if getcommand(text) == singleradiocommand:
                self.basicradiocommand(message, text, singleradiocommand, True)
        for radiostream in list(radiostreams.values()):
            if radiostream == getcommand(text):
                StickerController.sendstickerwithid(message.chat_id(), radiostream+".webp")

    def basicradiocommand(self, message, text, method_name, multiple_message):
        """
        Methodenrumpf für alle Radiocommands.
        Da alle Radiobefehle Streams als Parameter benötigen, wird dieser hier direkt weitergegeben.
        Außerdem wird hier zwischen Befehlen unterschieden,
        die entweder nur eine oder mehrere Nachrichten verschicken können.
        Ein Sendeplanbefehl muss beispielsweise für jeden Stream eine Nachricht verschicken,
        wo es andererseits beim Listenerbefehl reicht wenn alle Streams in eine Nachricht gepackt werden.
        :param message: Die verschickte Nachricht
        :param text: Der verschickte Text
        :param method_name: Name des Befehls und der Funktion
        :param multiple_message: Booleanwert der auf wahrgestellt wird,
        wenn jeweils eine Nachricht pro Stream geschickt werden soll
        """
        try:
            parameter = getparameter(text, self.chat)
            reply = ""
            if "wao" in parameter or "all" in parameter:
                if multiple_message:
                    for stream in radiostreams.values():
                        reply = getattr(self, method_name)(stream)
                        MessageController.sendreply(message, message.chat_id(), reply + "#%s" % method_name)
                else:
                    for stream in radiostreams.values():
                        reply += getattr(self, method_name)(stream)
                    MessageController.sendreply(message, message.chat_id(), reply + "#%s" % method_name)
            elif not (any(radio in parameter for radio in list(radiostreams.values())) or any(
                        radio in parameter for radio in list(radiostreams.keys()))):
                MessageController.sendreply(message, message.chat_id(),
                                            "\U0000274CBitte den Radiostream als Parameter mitgeben!\n#" + method_name)
            else:
                if multiple_message:
                    for radiostream in radiostreams.items():
                        if radiostream[0] in parameter or radiostream[1] in parameter:
                            reply = getattr(self, method_name)(radiostream[1])
                            MessageController.sendreply(message, message.chat_id(), reply + "#%s" % method_name)
                else:
                    for radiostream in radiostreams.items():
                        if radiostream[0] in parameter or radiostream[1] in parameter:
                            reply += getattr(self, method_name)(radiostream[1])
                    MessageController.sendreply(message, message.chat_id(), reply + "#%s" % method_name)
        except TypeError as typo:
            logger.exception(typo)
            MessageController.sendreply(message, message.chat_id(), "Witzbold.")

    @staticmethod
    def montag(stream):
        showplan = waoParser.load(stream + "_shows")
        return getshowfromday(showplan, 0, stream)

    @staticmethod
    def dienstag(stream):
        showplan = waoParser.load(stream + "_shows")
        return getshowfromday(showplan, 1, stream)

    @staticmethod
    def mittwoch(stream):
        showplan = waoParser.load(stream + "_shows")
        return getshowfromday(showplan, 2, stream)

    @staticmethod
    def donnerstag(stream):
        showplan = waoParser.load(stream + "_shows")
        return getshowfromday(showplan, 3, stream)

    @staticmethod
    def freitag(stream):
        showplan = waoParser.load(stream + "_shows")
        return getshowfromday(showplan, 4, stream)

    @staticmethod
    def samstag(stream):
        showplan = waoParser.load(stream + "_shows")
        return getshowfromday(showplan, 5, stream)

    @staticmethod
    def sonntag(stream):
        showplan = waoParser.load(stream + "_shows")
        return getshowfromday(showplan, 6, stream)

    @staticmethod
    def heute(stream):
        showplan = waoParser.load(stream + "_shows")
        return getshowfromtoday(showplan, stream)

    @staticmethod
    def morgen(stream):
        showplan = waoParser.load(stream + "_shows")
        return getshowfromtomorrow(showplan, stream)

    @staticmethod
    def next(stream):
        showplan = waoParser.load(stream + "_shows")
        return nextshow(showplan, stream)

    @staticmethod
    def track(stream):
        artist = waoParser.getjsonelement(stream + "_onAir", "artist")
        track = waoParser.getjsonelement(stream + "_onAir", "track")
        return str('''%sAktueller Track @ %s: %s - %s
''' % (emoji.musical_note,stream.capitalize(), artist, track))

    @staticmethod
    def dj(stream):
        dj = waoParser.getjsonelement(stream + "_onAir", "dj")
        djid = waoParser.getjsonelement(stream + "_onAir", "djid")
        if dj:
            return str('''%sAktueller DJ @ %s: %s
''' % (emoji.microphone,stream.capitalize(), getdjnamebyonair(dj, djid)))
        else:
            return str('''%sKein DJ ON AIR @ %s!
''' % (emoji.thumb_down,stream.capitalize()))

    @staticmethod
    def listener(stream):
        listener = waoParser.getjsonelement(stream + "_onAir", "listener")
        return str('''%sAktuelle Listeneranzahl @ %s: %s
''' % (emoji.satellite,stream.capitalize(), listener))

    @staticmethod
    def now(stream):
        dj = waoParser.getjsonelement(stream + "_onAir", "dj")
        djid = waoParser.getjsonelement(stream + "_onAir", "djid")
        show = waoParser.getjsonelement(stream + "_onAir", "show")
        style = waoParser.getjsonelement(stream + "_onAir", "style")
        start = waoParser.getjsonelement(stream + "_onAir", "start")
        end = waoParser.getjsonelement(stream + "_onAir", "end")
        if dj:
            return str('''%sAktuelle Show-Info @ %s%s
%sDJ: %s
%sShowname: %s
%sStyle: %s
%sUhrzeit: %s:00 bis %s:00
''' % (emoji.info_button,stream.capitalize(),emoji.info_button,emoji.microphone,
       getdjnamebyonair(dj, djid),emoji.loudspeaker, show,emoji.headphone, style,emoji.alarm_clock, start, end))
        else:
            return str('''%sAktuelle Show-Info @ %s%s
%sKein DJ ON AIR!
''' % (emoji.info_button,stream.capitalize(),emoji.info_button,emoji.thumb_down))
