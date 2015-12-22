# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.bot.commands import *
from telegram.basicapi.commands import sendreply,senddocument,sendtext
import uwsgi
from telegram.tgredis import setfilevalue, deleteentryfromfile
from resources import emoji
from telegram.basicapi.decorator.permissions import admin
from telegram.basicapi.decorator.tgcommands import reply,text


class AdminCommands:
    @admin
    def restart(self,message):
        """
        Startet den Bot neu.
        :param message: Die gesendete Nachricht
        """
        logger.debug("Server will shutdown!")
        sendreply(message, message.chat_id(),
                                    "%sIch - der WeAreOne Bot - werde jetzt neu gestartet.%s"
                                    % (emoji.warning,emoji.warning))
        uwsgi.reload()

    @admin
    @reply
    def reggroup(self,message):
        """
        Diese Methode registriert die Gruppe mit dem Bot, in der die Nachricht geschrieben wurde
        :param message: Die gesendete Nachricht
        """
        chat = message.chat
        value = {"title": chat.title}
        logger.debug("VALUE: " + str(value))
        setfilevalue("groups", message.chat_id(), value)
        return (message.chat_id(),
                "Der Gruppenchat " + value["title"] + " wurde erfolgreich registriert.")

    @admin
    @reply
    def unreggroup(self,message):
        """
        Die angeschriebene Gruppen wird ausgetragen, die Registrierung gelöscht
        :param message: Die gesendete Nachricht
        """
        user = message.from_User
        deleteentryfromfile("groups", message.chat_id())
        return (message.chat_id(),
                user.first_name + ", du hast die Gruppe aus den registrierten Gruppen gelöscht.")

    @admin
    def error(self,message):
        file = open("/home/tgbot/telegrambot_files/log/errorlog")
        senddocument(message.chat_id(),"error.log",file)

    @admin
    @reply
    def grouptype(self,message):
        """
        Zuteilung von Streams zu einer Gruppe
        :param message: Die gesendete Nachricht
        """
        param = getparameter(message.text)
        chat = message.chat
        values = getfilevalue("groups", message.chat_id())
        logger.debug("VALUE GROUPTYPE: " + str(values))
        if param:
            if not values:
                dump = {"title": chat.title, "type": param}
                setfilevalue("groups", message.chat_id(), dump)
            else:
                values["type"] = param
                setfilevalue("groups", message.chat_id(), values)

            return (message.chat_id(),
                    emoji.check_mark + "Gruppentyp wurde auf " + param + " gesetzt.")
        else:
            try:
                del values["type"]
                setfilevalue("groups", message.chat_id(), values)
                return (message.chat_id(),
                         emoji.check_mark+"Typenparameter für " + values["title"] + " zurückgesetzt.")
            except KeyError as error:
                logger.warn(str(error) + " - Eintrag in dem Dictionary nicht vorhanden.")
            except TypeError as error:
                logger.warn(str(error) + " - Eintrag in dem Dictionary nicht vorhanden.")

    @admin
    @reply
    def groupstream(self,message):
        """
        Zuteilung von Streams zu einer Gruppe
        :param message: Die gesendete Nachricht
        """
        param = getparameter(message.text)
        chat = message.chat
        values = getfilevalue("groups", message.chat_id())
        logger.debug("VALUE GROUPSTREAM: " + str(values))
        if param:
            if not values:
                dump = {"title": chat.title, "stream": param}
                setfilevalue("groups", message.chat_id(), dump)
            else:
                values["stream"] = param
                setfilevalue("groups", message.chat_id(), values)

            return (message.chat_id(),
                    emoji.check_mark + "Stream der Gruppe wurde auf " + param + " gesetzt.")
        else:
            try:
                del values["stream"]
                setfilevalue("groups", message.chat_id(), values)
                return (message.chat_id(),
                         emoji.check_mark+"Streamparameter für " + values["title"] + " zurückgesetzt.")
            except KeyError as error:
                logger.warn(str(error) + " - Eintrag in dem Dictionary nicht vorhanden.")
            except TypeError as error:
                logger.warn(str(error) + " - Eintrag in dem Dictionary nicht vorhanden.")

    @admin
    @text
    def testchannel(self,message):
        param = getparameter(message.text,None)
        json = sendtext(param,"Testing Channel...")
        logger.debug("JSON: "+str(json))

        return message.chat_id(),"ID: "+ str(json["result"]["chat"]["id"])
