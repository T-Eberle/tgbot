# -*- coding: utf-8 -*-
__author__ = 'Thomas'

import re

import telegram.bot.parser.commandparser as commandparser
import telegram.bot.parser.textparser as textparser
from telegram.bot.commands.admincommands import *
from telegram.bot.parser import *
from telegram.bot.updater import *
from telegram.tgredis import *
from telegram.config.jsonconfigreader import JSONConfigReader

jsongroups = JSONConfigReader("groups")


def parseMessage(message):
    chat = message.chat
    user = message.from_User
    updategroup(message)
    if message.text:
        if message.text.lower()=="/me":
            meCommand(message)
        elif message.text is not None and isPermitted(message):
            logger.debug("Trying to get users.")
            updateuser(user)
            if any("/"+admin in message.text.lower() for admin in admincommands) and isAdmin(message):
                admCommands = AdminCommands()
                admCommands.parseadmincommands(message,message.text)
            if re.match(r'/(\w)*', message.text):
                commandparser.parsecommand(message)
            else:
                textparser.parsetext(message)

def meCommand(message):
    user = message.from_User
    logger.debug("Befehl /me erkannt.")
    MessageController.sendreply(message, message.chat_id(),
                                    "\u2139" + "Daten über dich\u2139 \n" +
                                    "\U0001F539" + " Vorname: " + user.first_name + "\n" +
                                    "\U0001F539" + " Nachname: " + user.last_name + "\n" +
                                    "\U0001F539" + " Username: @" + user.username + "\n" +
                                    "\U0001F539" + " Chat ID: " + str(user.chat_id))



