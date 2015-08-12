# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'
from telegram.tglogging import logger
from telegram.bot.commands import *
from telegram.config.jsonconfigreader import JSONConfigReader
from telegram.basicapi.commands.messagecommands import MessageController


admincommands = ["reggroup","unreggroup","unregisterall"]


jsongroups = JSONConfigReader("groups")
jsonusers = JSONConfigReader("users")

class AdminCommands:

    def parseadmincommands(self,message,text):
        logger.debug(text+" command recognized.")
        for registercommand in admincommands:
            if getcommand(text)==registercommand:
                getattr(self, registercommand)(message,text)

    def reggroup(self,message,text):
        chat = message.chat
        value = chat.title
        logger.debug("TITLE: "+value)
        jsongroups.write(message.chat_id(),value)
        MessageController.sendreply(message, message.chat_id(), "Der Gruppenchat "+value+" wurde erfolgreich registriert.")

    def unreggroup(self,message,text):
        user = message.from_User
        jsongroups.deleteall()
        MessageController.sendreply(message, message.chat_id(), user.first_name+", du hast alle Users gelöscht. Sei stolz auf dich.")


    def unregisterall(self,message,text):
        user = message.from_User
        jsonusers.deleteall()
        MessageController.sendreply(message, message.chat_id(), user.first_name+", du hast alle Users gelöscht. Sei stolz auf dich.")


