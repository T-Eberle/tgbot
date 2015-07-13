__author__ = 'Thomas'

import telegram.bot.weareone.parser.commandparser as commandparser
import re

def parseMessage(message):
    chat = message.chat
    user = message.from_User

    if re.match(r'/(\w)*',message.text):
        commandparser.parsecommand(message)
    else:
        pass