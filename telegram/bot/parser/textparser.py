# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.commands.entertaincommands import *
from telegram.tgredis import *


def parsetext(message):
    text = message.text.lower()

    if any(entertain in text for entertain in entertaincommands) and commandallowed(message):
        parseentertaintext(message)
