#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Thomas'

import re
from telegram.tglogging import logger
from telegram.tgredis import TGRedis
import inspect

regex = re.compile(r'/(?P<command>\w+)(\s(?P<parameter>.+))?')




def parsecommand(message,args):

    text = message.text
    logger.debug("PARSING COMMAND WITH TEXT:" +text)

    if re.match(r'/(\w)+', message.text):
        command = getcommand(text)
    elif TGRedis.getconvcommand(message):
        logger.debug("COMMAND FROM REDIS: "+TGRedis.getconvcommand(message))
        command = TGRedis.getconvcommand(message)
    else:
        return
    logger.debug("FOUND COMMAND: "+command)
    if args:
        for obj in args:
            if inspect.getmembers(obj):
                for method in inspect.getmembers(obj):
                    if command.lower() == method[0]:
                        logger.info(command + " command recognized.")
                        getattr(obj,method[0])(message)
