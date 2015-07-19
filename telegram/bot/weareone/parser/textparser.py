__author__ = 'Thomas'

from telegram.bot.weareone.commands.entertaincommands import *


def parsetext(message):
    chat = message.chat
    user = message.from_User
    text = message.text.lower()

    if any(entertain in text for entertain in entertaincommands):
        parseentertaintext(message)
