# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.tglogging import *
from telegram.basicapi.commands.messagecommands import MessageController
from telegram.tgredis import getfilevalue
from resources import emoji
from telegram.basicapi.commands.filecommands import FileController


def me(message):
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
            extrainfos += emoji.blue_diamond + " WeAreOne-ID: " + value.get("wao_id") + "\n"
        if value.get("stream"):
            extrainfos += emoji.blue_diamond + " Streams: " + value.get("stream") + "\n"

    MessageController.sendreply(message, message.chat_id(),
                                emoji.info_button + "Daten über dich" + emoji.info_button + "\n" +
                                emoji.blue_diamond + " Vorname: " + user.first_name + "\n" +
                                emoji.blue_diamond + " Nachname: " + user.last_name + "\n" +
                                emoji.blue_diamond + " Username: @" + user.username + "\n" +
                                emoji.blue_diamond + " Chat ID: " + str(user.chat_id) + "\n" + extrainfos)


def helpme(message):
    """
    Funktion, die dem Nutzer Hilfe zum Nutzen des Bots anbietet.
    :param message: Die vom Nutzer gesendete Nachricht
    """
    FileController.senddocument(message.chat_id(),"TG-Bot-Manual.pdf")
    # MessageController.sendreply(message, message.chat_id(),
    #                             emoji.info_button + "Hilfe bekommst du in der PDF-Datei auf unserer Cloud.\n" +
    #                             "https://cloud.tb-group.fm/")
