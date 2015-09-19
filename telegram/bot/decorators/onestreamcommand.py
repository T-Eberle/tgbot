# -*- coding: utf-8 -*-
__author__ = 'Tommy'

from telegram.bot.commands import getparameter,getstreamparameter
import re
from telegram.tgredis import addtoconv, deleteconv
from telegram.basicapi.commands.messagecommands import MessageController
from telegram.tglogging import logger

radiostreams = {"tb": "technobase", "ht": "housetime", "hb": "hardbase", "trb": "trancebase", "ct": "coretime",
                         "clt": "clubtime"}

def onestreamcommand(func):
    def _wrapper(*args):
        regex = re.compile(r'(\b(ht|ct|clt|tb|hb|coretime|housetime|technobase|trancebase|clubtime|hardbase)\b)')
        obj = args[0]
        message = args[1]
        text = message.text
        chat = getstreamparameter(message)
        parameter = getparameter(text,chat).lower()
        result = regex.search(parameter)
        if not parameter and not result:
                keyboard = [["Technobase","Housetime","Hardbase"],["Coretime","Clubtime","Trancebase"]]
                MessageController.sendreply_one_keyboardmarkup(message,message.chat_id(),
                                                               "\U0000274CBitte wähle einen Radiostream aus.\n/" +
                                                               func.__name__,keyboard)
                addtoconv(message,"/" + func.__name__)
        else:
            logger.debug("RESULT REGEX: "+str(result.group(0)))
            if result.group(0) in radiostreams.keys():
                logger.debug("ITS A KEY!")
                obj.radiostream = radiostreams.get(result.group(0))
            else:
                obj.radiostream = result.group(0)
            reply = func(*args)[1]
            MessageController.hide_keyboard(message, message.chat_id(), reply + "#%s" % func.__name__)
            deleteconv(message)
    return _wrapper
