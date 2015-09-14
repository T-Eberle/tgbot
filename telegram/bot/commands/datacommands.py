# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.tglogging import *
from telegram.tgredis import getfilevalue
from resources import emoji
from telegram.basicapi.commands.filecommands import FileController
from telegram.config.waoapiparser import WAOAPIParser
from telegram.config.tgbotconfigparser import TGBotConfigParser
from datetime import datetime
from telegram.basicapi.decorator.tgcommands import sendreply
from telegram.basicapi.decorator.permissions import botonly


waoconfig = TGBotConfigParser("wao-config.ini")
waodata = waoconfig.load()


class DataCommands:
    @botonly
    @sendreply
    def me(self,message):
        """
        Gibt als String Daten von dem Nutzer zurück, unter Anderem:
        - Vorname
        - Nachname
        - Chat-Id
        - WAO-ID, falls vorhanden
        - Stream, falls vorhanden
        :param message: Die vom Nutzer gesendete Nachricht
        """
        user = message.from_User
        logger.debug("Befehl /me erkannt.")
        try:
            value = getfilevalue("users", user.getchatid())
        except KeyError:
            value = None
        extrainfos = ""
        if not value:
            logger.debug("User " + str(user.getchatid()) + " is not registered.")
        else:
            if value.get("wao_id"):
                logger.debug("User " + str(user.getchatid()) + " is registered.")
                extrainfos += emoji.blue_diamond + " WeAreOne-ID: " + value.get("wao_id") + "\n"\
                              + emoji.blue_diamond + " [Profile Picture]"\
                              + "(http://p.image.web.tb-group.fm/profile/profil_small"\
                              + value.get("wao_id") + ")\n"
            if value.get("stream"):
                extrainfos += emoji.blue_diamond + " Streams: " + value.get("stream") + "\n"
        user = message.from_User
        return (user.chat_id,
                emoji.info_button + "*Daten über dich*" + emoji.info_button + "\n" +
                emoji.blue_diamond + " _Vorname:_ " + user.first_name + "\n" +
                emoji.blue_diamond + " _Nachname:_ " + user.last_name + "\n" +
                emoji.blue_diamond + " _Username:_ @" + user.username + "\n" +
                emoji.blue_diamond + " _Chat ID:_ " + str(user.chat_id) + "\n" + extrainfos)

    @staticmethod
    def start(self,message):
        FileController.senddocument(message.chat_id(),"TG-Bot-Manual.pdf")

    @staticmethod
    def hilfe(message):
        """
        Funktion, die dem Nutzer Hilfe zum Nutzen des Bots anbietet.
        :param message: Die vom Nutzer gesendete Nachricht
        """
        FileController.senddocument(message.chat_id(),"TG-Bot-Manual.pdf")

    @sendreply
    def keyboard(self,message):
        waoapiparser = WAOAPIParser(stream="housetime")
        shows = waoapiparser.loadwaoapishowplan(site=2,count=2,upcoming=True)
        if len(shows) == 2:
            show_1 = shows[0]
            show_2 = shows[1]
            now = datetime.now().date()
            start_1 = WAOAPIParser.correcdate(show_1[waodata.get("waoapi-showplan","start")])
            end_1 = WAOAPIParser.correcdate(show_1[waodata.get("waoapi-showplan","end")])
            start_2 = WAOAPIParser.correcdate(show_2[waodata.get("waoapi-showplan","start")])
            if start_1.date() - now == 0 and end_1 == start_2:
               return(message.chat_id(),'''%sÜbergabeprotokoll%s.
    Size: %s''' % (emoji.warning,emoji.warning,str(show_1[waodata.get("waoapi-showplan","show")])))
            else:
                 return(message.chat_id(),'''%sÜbergabeprotokoll%s.
                 Gibt's nicht.''' % (emoji.warning,emoji.warning,))
