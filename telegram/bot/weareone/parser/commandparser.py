#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.basicapi.commands.messagecommands import MessageController
def parsecommand(message):
    chat = message.chat
    user = message.from_User
    text = message.text.replace("/", "")

    if "deinemudda" == text:
        MessageController.sendMessage(message,message.chat_id(),"Command für deine Mutter Witze \n Noch nicht implementiert.")
    elif "listeners" == text:
        MessageController.sendMessage(message,message.chat_id(),"Command für Anzeige der Listener \n Noch nicht implementiert.")
    elif "now" == text:
        MessageController.sendMessage(message,message.chat_id(),"Command für Anzeige des aktuellen DJs \n Noch nicht implementiert.")
    elif "sendeplan" ==text:
        MessageController.sendMessage(message,message.chat_id(),"Command für Anzeige eines Sendeplantages in der Woche \n Noch nicht implementiert.")
    elif "dj" ==text:
        MessageController.sendMessage(message,message.chat_id(),"Command für momentan auflegenden DJ \n Noch nicht implementiert.")
    elif "email" == text:
        MessageController.sendMessage(message,message.chat_id(),"Command für Emaildaten eines Members \n Noch nicht implementiert.")
    elif "contact" == text:
        MessageController.sendMessage(message,message.chat_id(),"Command für Kontaktdaten eines Members \n Noch nicht implementiert.")
