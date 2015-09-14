# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.parser import commandparser
from telegram.bot.parser import textparser
from telegram.bot.updater import *
from telegram.tgredis import *
from telegram.bot.commands.admincommands import AdminCommands
from telegram.bot.commands.datacommands import *
from telegram.bot.commands.entertaincommands import EntertainCommands
from telegram.bot.commands.radiocommands import RadioCommands
from telegram.bot.commands.registercommands import RegisterCommands
from telegram.basicapi.decorator.permissions import *


#TODO VERY DIRTY: Das muss noch geändert werden!!!!
#Speichern der Conversations mit Redis?
def parsereplycommand(message):
    match_text = re.search(r'/(\w)+',message.text)
    conv = getconv(message)
    logger.info("CONVERSATION: " + str(conv))
    if conv != "None" and not match_text:
        match = re.search(r'/(\w)+',conv)
        if match:
            parameter = message.text
            message.text = match.group() + " " + parameter
    elif conv != "None" and message.text == "/cancel":
        deleteconv(message)
        MessageController.hide_keyboard(message,message.chat_id(),"Du willst mit mir die Konversation abbrechen? "
                                                                  "Alles klar....")
    elif conv != "None" and match_text:
        deleteconv(message)

    logger.info("OFFICIAL MESSAGE: " + message.text)


@permitted
def parsemessage(message):
    user = message.from_User
    updategroup(message)
    parsereplycommand(message)
    if message.text is not None:
        logger.debug("Trying to get users.")
        updateuser(user)
        if re.match(r'/(\w)+', message.text):
                commandparser.parsecommand(message,RadioCommands(),RegisterCommands(),DataCommands(),
                                           EntertainCommands(),AdminCommands())
        else:
            textparser.parsetext(message)
