# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.parser import commandparser
from telegram.bot.parser import textparser
from telegram.bot.updater import *
from telegram.tgredis import *
from telegram.tglogging import *
from telegram.bot.commands.admincommands import AdminCommands,admincommands
import re
from telegram.bot.commands.datacommands import *

config = TGBotConfigParser("config.ini")
data = config.load()

def isPermitted(message):
    if isAdmin(message) or isPermittedGroup(message):
        return True
    else:
        return False

def isAdmin(message):
    user = message.from_User
    if str(user.chat_id) in data.get("basics","superadmins"):
        logger.debug("@"+user.username+"("+str(user.chat_id)+") ist ein SuperAdmin.")
        return True
    else:
        return False
        logger.debug("@"+user.username+"("+str(user.chat_id)+") ist kein SuperAdmin")

def isPermittedGroup(message):
    groups = getfile("groups")
    logger.debug("Is this a permitted group? "+str(message.chat_id()))
    logger.debug("Permitted Chat_Ids:"+str(groups.keys()))
    if str(message.chat_id()) in groups.keys():
        logger.debug("PERMITTED GROUP CHAT: "+ str(message.chat_id()))
        return True
    else:
        return False



def parseMessage(message):
    chat = message.chat
    user = message.from_User
    updategroup(message)
    if message.text is not None and isPermitted(message):
            logger.debug("Trying to get users.")
            updateuser(user)
            if any("/"+admin in message.text.lower() for admin in admincommands) and isAdmin(message):
                admCommands = AdminCommands()
                admCommands.parseadmincommands(message,message.text)
            elif re.match(r'/(\w)*', message.text):
                if message.text.lower()=="/hilfe":
                    help(message)
                elif message.text.lower()=="/me":
                    me(message)
                else:
                    commandparser.parsecommand(message)
            else:
                textparser.parsetext(message)


