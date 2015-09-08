# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.tglogging import *
from telegram.basicapi.commands.messagecommands import MessageController
from telegram.tgredis import getfilevalue
from resources import emoji
from telegram.basicapi.commands.filecommands import FileController
from telegram.bot.commands import getparameter


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
            extrainfos += emoji.blue_diamond + " WeAreOne-ID: " + value.get("wao_id") + "\n"+\
                          emoji.blue_diamond + " [Profile Picture]" +"(http://p.image.web.tb-group.fm/profile/profil_small"\
                          + value.get("wao_id")+")\n"
        if value.get("stream"):
            extrainfos += emoji.blue_diamond + " Streams: " + value.get("stream") + "\n"

    MessageController.sendreply(message, message.chat_id(),
                                emoji.info_button + "*Daten über dich*" + emoji.info_button + "\n" +
                                emoji.blue_diamond + " _Vorname:_ " + user.first_name + "\n" +
                                emoji.blue_diamond + " _Nachname:_ " + user.last_name + "\n" +
                                emoji.blue_diamond + " _Username:_ @" + user.username + "\n" +
                                emoji.blue_diamond + " _Chat ID:_ " + str(user.chat_id) + "\n" + extrainfos)


def helpme(message):
    """
    Funktion, die dem Nutzer Hilfe zum Nutzen des Bots anbietet.
    :param message: Die vom Nutzer gesendete Nachricht
    """
    FileController.senddocument(message.chat_id(),"TG-Bot-Manual.pdf")


def keyboard(message):
    if message.reply_to_message:
        MessageController.hide_Keyboard(message,message.chat_id(),"Wow, dein Liebliengsstream ist "+getparameter(message.text)+"? Hammer.")
    else:
        keyboard= [["Housetime"],["Technobase"],["Hardbase"],["Clubtime"],["Coretime"],["Trancebase"]]
        MessageController.sendreply_one_keyboardmarkup(message,message.chat_id(),"Welcher ist dein Lieblingsstream? /keyboard",keyboard)
