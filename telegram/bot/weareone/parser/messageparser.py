__author__ = 'Thomas'

import telegram.bot.weareone.parser.commandparser as commandparser
import telegram.bot.weareone.parser.textparser as textparser
import re


def parseMessage(message):
    chat = message.chat
    user = message.from_User

    if message.text is not None:

        if re.match(r'/(\w)*', message.text):
            commandparser.parsecommand(message)
        else:
            textparser.parsetext(message)
