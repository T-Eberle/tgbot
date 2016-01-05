# -*- coding: utf-8 -*-
__author__ = 'Thomas'

import re

from resources import emoji
from telegram.basicapi.commands import sendreply
from telegram.basicapi.parser import commandparser
from telegram.basicapi.parser import textparser,inlineparser
from telegram.tgredis import *

wartungsmodus = False
regex = re.compile(r'/(?P<command>\w+)(\s(?P<parameter>.+))?')
config = TGBotConfigParser("config.ini")
data = config.load()

def isadmin(message):
        user = message.from_User
        if str(user.chat_id) in data.get("basics", "superadmins"):
            logger.debug("@" + user.username + "(" + str(user.chat_id) + ") ist ein SuperAdmin.")
            return True
        else:
            logger.debug("@" + user.username + "(" + str(user.chat_id) + ") ist kein SuperAdmin")
            return False

def parsemessage(message,wartungsmodus,args):
    user = message.from_User
    # parsereplycommand(message)
    if message.text is not None:
        #WARTUNGSMODUS
        if wartungsmodus and not isadmin(message):
            sendreply(message,message.chat_id(),emoji.warning+"ICH WERDE GERADE GEWARTET!")
            return
        #WARTUNGSMODUS ENDE
        if re.match(r'/(\w)+', message.text):
                commandparser.parsecommand(message,args)
        elif TGRedis.getconvcommand(message):
                commandparser.parsecommand(message,args)
        else:
            textparser.parsetext(message)


def parseinline(inline,args):
    # parsereplycommand(message)
    if inline.query is not None:
            inlineparser.parseinline(inline,args)
