# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.parser import commandparser
from telegram.bot.parser import textparser
from telegram.bot.updater import *
from telegram.tgredis import *
from telegram.basicapi.model.message import Message
from telegram.bot.commands.admincommands import AdminCommands
from telegram.bot.commands.datacommands import *
from telegram.bot.commands.entertaincommands import EntertainCommands
from telegram.bot.commands.radiocommands import RadioCommands
from telegram.bot.commands.registercommands import RegisterCommands
from telegram.basicapi.decorator.permissions import func_isadmin




def ispermitted(message):
    if  ispermittedgroup(message):
        return True
    elif func_isadmin(message):
        return True
    else:
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
        if re.match(r'/(\w)+', message.text):
                commandparser.parsecommand(message,RadioCommands(),RegisterCommands(),DataCommands(),EntertainCommands(),AdminCommands())
        else:
            textparser.parsetext(message)
