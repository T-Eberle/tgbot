#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.commands.radiocommands import *
import inspect


def parsecommand(message,*args):
    text = message.text
    command = getcommand(text)
    for obj in args:
            logger.debug(command + " command recognized.")
            for method in inspect.getmembers(obj):
                if getcommand(text).lower() == method[0]:
                    getattr(obj,method[0])(message)
