#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.weareone.commands.radiocommands import *
from telegram.bot.weareone.commands.datacommands import *
from telegram.bot.basicapi.commands.messagecommands import MessageController
from telegram.bot.tglogging.TGLogger import logger
import codecs

def parsecommand(message):
    chat = message.chat
    user = message.from_User
    text = message.text.replace("/", "")

    if(text in radiocommands):
        parseradiocommands(message,text)
    elif "deinemudda" == text:
        MessageController.sendmessage(message, message.chat_id(),
                                      "Command für deine Mutter Witze \n Noch nicht implementiert.")
    elif "email" == text:
        MessageController.sendreply(message, message.chat_id(),
                                    "\U0001F4E7" + "Emailaddresse von @" + user.username + ": " + user.first_name + "@imakeyousexy.com \n")
    elif "contact" == text:
        MessageController.sendmessage(message, messagels .chat_id(),
                                      "Command für Kontaktdaten eines Members \n Noch nicht implementiert.")
    elif "me" == text:
        logger.debug("Befehl /me erkannt.")
        MessageController.sendreply(message, message.chat_id(),
                                    "\u2139" + "Daten über dich\u2139 \n" +
                                    "\U0001F539" + " Vorname: " + user.first_name + "\n" +
                                    "\U0001F539" + " Nachname: " + user.last_name + "\n" +
                                    "\U0001F539" + " Username: @" + user.username + "\n" +
                                    "\U0001F539" + " Chat ID: " + str(user.chat_id))
