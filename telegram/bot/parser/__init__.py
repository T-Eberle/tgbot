# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.parser import commandparser
from telegram.bot.parser import textparser
from telegram.bot.updater import *
from telegram.tgredis import *
from telegram.basicapi.model.message import Message
from telegram.bot.commands.admincommands import AdminCommands, admincommands
from telegram.bot.commands.datacommands import *
from telegram.bot.commands.entertaincommands import macarena

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

#TODO VERY DIRTY: Das muss noch geändert werden!!!!
#Speichern der Conversations mit Redis?
def parsereplycommand(message):
    match_text = re.search(r'/(\w)+',message.text)
    conv = getconv(message)
    logger.info("CONVERSATION: "+str(conv))
    if conv!="None" and not match_text:
        match = re.search(r'/(\w)+',conv)
        if match:
            parameter = message.text
            message.text = match.group()+" "+parameter
    elif conv!="None" and message.text=="/cancel":
        deleteconv(message)
        MessageController.hide_Keyboard(message,message.chat_id(),"Du willst mit mir die Konversation abbrechen? "
                                                                  "Alles klar....")
    elif conv!="None" and match_text:
        deleteconv(message)

    logger.info("OFFICIAL MESSAGE: "+message.text)

def parsemessage(message):
    user = message.from_User
    updategroup(message)
    parsereplycommand(message)
    if message.text is not None and ispermitted(message):
        logger.debug("Trying to get users.")
        updateuser(user)
        if any("/" + admin in message.text.lower() for admin in admincommands) and isadmin(message):
            admcommands = AdminCommands()
            admcommands.parseadmincommands(message)
        if "/keyboard" in message.text.lower():
                keyboard(message)
        elif re.match(r'/(\w)+', message.text):
            if message.text.lower() == "/macarena":
                macarena(message)
            if message.text.lower() == "/hilfe":
                helpme(message)
            elif message.text.lower() == "/me":
                me(message)
            else:
                commandparser.parsecommand(message)

        else:
            textparser.parsetext(message)
