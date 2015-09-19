#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.commands.radiocommands import *
import inspect


def parsecommand(message,*args):
    text = message.text
    command = getcommand(text)
    for obj in args:
            for method in inspect.getmembers(obj):
                if getcommand(text).lower() == method[0]:
                    logger.info(command + " command recognized.")
                    getattr(obj,method[0])(message)
