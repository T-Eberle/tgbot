# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'


from telegram.tglogging import *
from telegram.basicapi.commands.messagecommands import MessageController
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.config.jsonconfigreader import JSONConfigReader
import json
from telegram.tgredis import getfilevalue



def me(message):
    user = message.from_User
    logger.debug("Befehl /me erkannt.")
    try:
        value = getfilevalue("users",user.getchatid())
    except KeyError as error:
        value=None
    extrainfos = ""
    if not value:
        logger.debug("User "+str(user.getchatid())+" is not registered.")
    else:
        if value.get("wao_id"):
            logger.debug("User "+str(user.getchatid())+" is registered.")
            extrainfos+= "\U0001F539" + " WeAreOne-ID: " + value.get("wao_id") + "\n"
        if value.get("stream"):
            extrainfos+= "\U0001F539" + " Streams: " + value.get("stream") + "\n"

    MessageController.sendreply(message, message.chat_id(),
                                        "\u2139" + "Daten über dich\u2139 \n" +
                                        "\U0001F539" + " Vorname: " + user.first_name + "\n" +
                                        "\U0001F539" + " Nachname: " + user.last_name + "\n" +
                                        "\U0001F539" + " Username: @" + user.username + "\n" +
                                        "\U0001F539" + " Chat ID: " + str(user.chat_id)+"\n"+extrainfos)

def help(message):
    MessageController.sendreply(message, message.chat_id(),"\U00002139Hilfe bekommst du in der PDF-Datei auf unserer Cloud.\n"+
                                "https://cloud.tb-group.fm/")