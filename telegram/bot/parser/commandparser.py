#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.commands.radiocommands import *
from telegram.bot.commands.registercommands import RegisterCommands,allRegcommands
from telegram.bot.commands.admincommands import *
from telegram.tglogging import logger


def parsecommand(message):
    chat = message.chat
    user = message.from_User
    text = message.text

    if any("/"+radio in text for radio in allradiocommands):
        radcommands = RadioCommands()
        radcommands.parseradiocommands(message,text)
    elif any("/"+register in text for register in allRegcommands):
        regcommands = RegisterCommands()
        regcommands.parseregistercommands(message,text)


