__author__ = 'Thomas'

import re
from telegram.bot.basicapi.commands.messagecommands import MessageController
import telegram.bot.weareone.parser.commandparser as commandparser

def parseMessage(message):
    chat = message.chat
    user = message.from_User

    if re.match(r'/(\w)*',message.text):
        commandparser.parsecommand(message)
    else:
        pass