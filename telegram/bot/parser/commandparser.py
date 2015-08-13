#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.commands.radiocommands import *
from telegram.bot.commands.registercommands import RegisterCommands,allRegcommands
from telegram.bot.commands.admincommands import *
from telegram.tgredis import *
from telegram.tglogging import logger


def parsecommand(message):
    chat = message.chat
    user = message.from_User
    text = message.text

    if any("/"+radio in text.lower() for radio in allradiocommands) and commandAllowed(message):
        radcommands = RadioCommands()
        radcommands.parseradiocommands(message,text)
    elif any("/"+register in text.lower() for register in allRegcommands):
        regcommands = RegisterCommands()
        regcommands.parseregistercommands(message,text)


