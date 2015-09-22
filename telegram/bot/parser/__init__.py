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
from telegram.basicapi.commands import hide_keyboard
from resources import emoji

args = [RadioCommands(),RegisterCommands(),DataCommands(),
                                           EntertainCommands(),AdminCommands()]

wartungsmodus = False

@permitted
def parsemessage(message):
    user = message.from_User
    updategroup(message)
    # parsereplycommand(message)
    if message.text is not None:
        logger.debug("Trying to get users.")
        updateuser(user)
        #WARTUNGSMODUS
        if wartungsmodus and not func_isadmin(message):
            sendreply(message,message.chat_id(),emoji.warning+"ICH WERDE GERADE GEWARTET!")
            return
        #WARTUNGSMODUS ENDE
        if re.match(r'/(\w)+', message.text):
                commandparser.parsecommand(message,*args)
        elif getconvcommand(message):
                commandparser.parsecommand(message,*args)
        else:
            textparser.parsetext(message)
