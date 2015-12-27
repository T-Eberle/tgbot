# -*- coding: utf-8 -*-
__author__ = 'Thomas'

import re

from resources import emoji
from telegram.basicapi.commands import sendreply
from telegram.basicapi.parser import commandparser
from telegram.basicapi.parser import textparser
from telegram.bot.decorators.permissions import func_isadmin
from telegram.tgredis import *

wartungsmodus = False


def parsemessage(message,wartungsmodus,args):
    user = message.from_User
    # parsereplycommand(message)
    if message.text is not None:
        logger.debug("Trying to get users.")
        #WARTUNGSMODUS
        if wartungsmodus and not func_isadmin(message):
            sendreply(message,message.chat_id(),emoji.warning+"ICH WERDE GERADE GEWARTET!")
            return
        #WARTUNGSMODUS ENDE
        if re.match(r'/(\w)+', message.text):
                commandparser.parsecommand(message,args)
        elif TGRedis.getconvcommand(message):
                commandparser.parsecommand(message,args)
        else:
            textparser.parsetext(message)
