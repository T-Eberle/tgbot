#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.bot.commands.radiocommands import *
import inspect


def parsecommand(message,*args):

    text = message.text
    logger.debug("PARSING COMMAND WITH TEXT:" +text)

    if re.match(r'/(\w)+', message.text):
        command = getcommand(text)
    elif getconvcommand(message):
        logger.debug("COMMAND FROM REDIS: "+getconvcommand(message))
        command = getconvcommand(message)
    else:
        return
    logger.debug("FOUND COMMAND: "+command)
    for obj in args:
        for method in inspect.getmembers(obj):
            if command.lower() == method[0]:
                logger.info(command + " command recognized.")
                getattr(obj,method[0])(message)
