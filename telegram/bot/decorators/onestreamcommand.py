# -*- coding: utf-8 -*-
__author__ = 'Tommy'

import re

import pkg_resources

from telegram.bot.commands import getparameter,getstreamparameter
from telegram.tgredis import deleteconv, setconvcommand,getconvcommand
from telegram.basicapi.commands import sendreply_one_keyboardmarkup,hide_keyboard,sendphoto_hidekeyboard
from telegram.tglogging import logger

radiostreams = {"tb": "technobase", "ht": "housetime", "hb": "hardbase", "trb": "trancebase", "ct": "coretime",
                         "clt": "clubtime","tt": "teatime"}

def onestreamcommand(func):
    def _wrapper(*args):
        regex = re.compile(r'(\b(ht|ct|clt|tb|hb|tt|teatime|coretime|housetime|technobase|trancebase|clubtime|hardbase)\b)')
        obj = args[0]
        message = args[1]
        if getconvcommand(message)==func.__name__ and regex.search(message.text.lower()):
                parameter = message.text.lower()
                deleteconv(message)
        else:
            text = message.text
            chat = getstreamparameter(message)
            parameter = getparameter(text,chat).lower()
        logger.debug("RESULT PARAMETER: "+parameter)
        result = regex.search(parameter)
        if not parameter and not result:
                keyboard = [["Technobase","Housetime","Hardbase"],["Coretime","Clubtime","Trancebase"]]
                sendreply_one_keyboardmarkup(message,message.chat_id(),
                                                               "\U0000274CBitte wähle einen Radiostream aus.\n/" +
                                                               func.__name__,keyboard)
                setconvcommand(message,func.__name__)
        else:
            if result:
                logger.debug("RESULT REGEX: "+str(result.group(0)))
                if result.group(0) in radiostreams.keys():
                    logger.debug("ITS A KEY!")
                    obj.radiostream = radiostreams.get(result.group(0)).lower()
                else:
                    obj.radiostream = result.group(0).lower()
                reply = func(*args)[1]
                photo = pkg_resources.resource_filename("resources.img", obj.radiostream+".png")
                logger.debug("PHOTO: "+str(photo))
                status = sendphoto_hidekeyboard(message,message.chat_id(),None,open(photo,"rb"),caption=reply)
                logger.debug("ONESTREAMCOMMAND STATUS: "+str(status))
                if status == 400:
                    hide_keyboard(message,message.chat_id(),reply)
                deleteconv(message)
            else:
                return
    return _wrapper
