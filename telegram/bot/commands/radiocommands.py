# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import collections

from telegram.basicapi.commands.stickercommands import StickerController
from telegram.bot.commands import *
from telegram.config.tgbotfileidparser import TGBotFileIDParser
from telegram.config.waoapiparser import WAOAPIParser
from telegram.tgredis import *
from resources import emoji

multipleradiocommands = ["listener", "dj", "now", "track", "next"]

singleradiocommands = ["heute", "morgen","gestern", "montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag",
                       "sonntag"]

unsorted_radiostreams = {"tb": "technobase", "ht": "housetime", "hb": "hardbase", "trb": "trancebase", "ct": "coretime",
                         "clt": "clubtime"}
radiostreams = collections.OrderedDict(sorted(unsorted_radiostreams.items()))

allradiocommands = multipleradiocommands + singleradiocommands + list(radiostreams.values())
waoParser = WAOAPIParser("housetime_onAir")

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
            parameter = getparameter(text, self.chat).lower()
            reply = ""
            if "wao" in parameter or "all" in parameter:
                if multiple_message:
                    for stream in radiostreams.values():
                        reply = getattr(self, method_name)(stream)
                        MessageController.hide_Keyboard(message, message.chat_id(), reply + "#%s" % method_name)
                        deleteconv(message)
                else:
                    for stream in radiostreams.values():
                        reply += getattr(self, method_name)(stream)
                    MessageController.hide_Keyboard(message, message.chat_id(), reply + "#%s" % method_name)
                    deleteconv(message)
            elif (not (any(radio in parameter.lower() for radio in list(radiostreams.values())) or any(
                        radio in parameter.lower() for radio in list(radiostreams.keys()))))or parameter.lower()=="markup":
                keyboard= [["Housetime"],["Technobase"],["Hardbase"],["Clubtime"],["Coretime"],["Trancebase"]]
                MessageController.sendreply_one_keyboardmarkup(message,message.chat_id(),
                                                "\U0000274CBitte wähle einen Radiostream aus.\n/"
                                                               + method_name
                                                ,keyboard)
                addtoconv(message,"/"+method_name)
            else:
                if multiple_message:
                    for radiostream in radiostreams.items():
                        if radiostream[0] in parameter.lower() or radiostream[1] in parameter:
                            reply = getattr(self, method_name)(radiostream[1])
                            MessageController.hide_Keyboard(message, message.chat_id(), reply + "#%s" % method_name)
                            deleteconv(message)
                else:
                    for radiostream in radiostreams.items():
                        if radiostream[0] in parameter.lower() or radiostream[1] in parameter:
                            reply += getattr(self, method_name)(radiostream[1])
                    MessageController.hide_Keyboard(message, message.chat_id(), reply + "#%s" % method_name)
                    deleteconv(message)
        except TypeError as typo:
            logger.exception(typo)
            MessageController.hide_Keyboard(message, message.chat_id(), "Witzbold.")
            deleteconv(message)

    @staticmethod
    def gestern(stream):
        return getshowfromday(None,stream)

    @staticmethod
    def montag(stream):
        return getshowfromday(0, stream)

    @staticmethod
    def dienstag(stream):
        return getshowfromday(1, stream)

    @staticmethod
    def mittwoch(stream):
        return getshowfromday(2, stream)

    @staticmethod
    def donnerstag(stream):
        return getshowfromday(3, stream)

    @staticmethod
    def freitag(stream):
        return getshowfromday(4, stream)

    @staticmethod
    def samstag(stream):
        return getshowfromday(5, stream)

    @staticmethod
    def sonntag(stream):
        return getshowfromday(6, stream)

    @staticmethod
    def heute(stream):
        return getshowfromtoday(stream)

    @staticmethod
    def morgen(stream):
        return getshowfromtomorrow(stream)

    @staticmethod
    def next(stream):
        return nextshow(stream)

    @staticmethod
    def track(stream):
        try:
            artist = WAOAPIParser.nowartist(stream)
            track =WAOAPIParser.nowtrack(stream)
            release =WAOAPIParser.nowrelease(stream)
            release_string =""
            if release!="0":
                release_string =str("Check: http://www.technobase.fm/release/%s\n" % release)
            return str("%sAktueller Track @ %s: %s - %s\n"% (emoji.musical_note,stream.capitalize(), artist, track))\
                   + release_string

        except KeyError as error:
            logger.exception(error)
            return str('''%sKein DJ ON AIR @ %s!
''' % (emoji.thumb_down,stream.capitalize()))



    @staticmethod
    def dj(stream):
        try:
            dj = WAOAPIParser.now(stream,"dj")
            djid = str(WAOAPIParser.now(stream,"djid"))
            return str('''%sAktueller DJ @ %s: %s
''' % (emoji.microphone,stream.capitalize(), getdjnamebyonair(dj, djid)))
        except KeyError:
            return str('''%sKein DJ ON AIR @ %s!
''' % (emoji.thumb_down,stream.capitalize()))


    @staticmethod
    def listener(stream):
        listener = waoParser.gettrayelement(stream + "_onAir", "listener")
        return str('''%s*Aktuelle Listeneranzahl* @ _%s_: %s
''' % (emoji.satellite,stream.capitalize(), listener))

    @staticmethod
    def now(stream):
        try:
            WAOAPIParser.now(stream,"playlist")
            return str('''%sAktuelle Show-Info @ %s%s
%sKein DJ ON AIR!
''' % (emoji.info_button,stream.capitalize(),emoji.info_button,emoji.thumb_down))
        except KeyError:
            dj = WAOAPIParser.now(stream,"dj")
            djid = str(WAOAPIParser.now(stream, "djid"))
            show = WAOAPIParser.now(stream,"show")
            style = WAOAPIParser.now(stream,"style")
            start = WAOAPIParser.nowstart_string(stream)
            end = WAOAPIParser.nowend_string(stream)
            if dj:
                return str('''%sAktuelle Show-Info @ %s%s
%sDJ: %s
%sShowname: %s
%sStyle: %s
%sUhrzeit: %s bis %s
''' % (emoji.info_button,stream.capitalize(),emoji.info_button,emoji.microphone,
       getdjnamebyonair(dj, djid),emoji.loudspeaker, show,emoji.headphone, style,emoji.alarm_clock, start, end))

