# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.commands.entertaincommands import *


def parsetext(message):
    chat = message.chat
    user = message.from_User
    text = message.text.lower()

    if any(entertain in text for entertain in entertaincommands):
        parseentertaintext(message)
