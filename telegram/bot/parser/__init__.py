# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.parser import commandparser
from telegram.bot.parser import textparser
from telegram.bot.updater import *
from telegram.tgredis import *
from telegram.bot.commands.admincommands import AdminCommands, admincommands
from telegram.bot.commands.datacommands import *

config = TGBotConfigParser("config.ini")
data = config.load()


def ispermitted(message):
    if isadmin(message) or ispermittedgroup(message):
        return True
    else:
        return False


def isadmin(message):
    user = message.from_User
    if str(user.chat_id) in data.get("basics", "superadmins"):
        logger.debug("@" + user.username + "(" + str(user.chat_id) + ") ist ein SuperAdmin.")
        return True
    else:
        logger.debug("@" + user.username + "(" + str(user.chat_id) + ") ist kein SuperAdmin")
        return False


def ispermittedgroup(message):
    groups = getfile("groups")
    logger.debug("Is this a permitted group? " + str(message.chat_id()))
    logger.debug("Permitted Chat_Ids:" + str(groups.keys()))
    if str(message.chat_id()) in groups.keys():
        logger.debug("PERMITTED GROUP CHAT: " + str(message.chat_id()))
        return True
    else:
        return False


def parsemessage(message):
    user = message.from_User
    updategroup(message)
    if message.text is not None and ispermitted(message):
        logger.debug("Trying to get users.")
        updateuser(user)
        if any("/" + admin in message.text.lower() for admin in admincommands) and isadmin(message):
            admcommands = AdminCommands()
            admcommands.parseadmincommands(message)
        elif re.match(r'/(\w)*', message.text):
            if message.text.lower() == "/hilfe":
                helpme(message)
            elif message.text.lower() == "/me":
                me(message)
            else:
                commandparser.parsecommand(message)
        else:
            textparser.parsetext(message)
