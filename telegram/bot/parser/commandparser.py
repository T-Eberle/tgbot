#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.commands.radiocommands import *
from telegram.bot.commands.registercommands import RegisterCommands, allRegcommands
from telegram.tgredis import *


def parsecommand(message):
    text = message.text

    if any("/" + radio in text.lower() for radio in allradiocommands) and commandallowed(message):
        radcommands = RadioCommands()
        radcommands.parseradiocommands(message, text)
    elif any("/" + register in text.lower() for register in allRegcommands):
        regcommands = RegisterCommands()
        regcommands.parseregistercommands(message, text)
