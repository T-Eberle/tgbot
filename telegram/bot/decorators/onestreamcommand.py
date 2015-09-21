# -*- coding: utf-8 -*-
__author__ = 'Tommy'

from telegram.bot.commands import getparameter,getstreamparameter
import re
from telegram.tgredis import addtoconv, deleteconv
from telegram.basicapi.commands import sendreply_one_keyboardmarkup,hide_keyboard,sendphoto_hidekeyboard
from telegram.tglogging import logger
import pkg_resources
from PIL import Image
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
                sendreply_one_keyboardmarkup(message,message.chat_id(),
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
            photo = pkg_resources.resource_filename("resources.img", obj.radiostream+".png")
            logger.debug("PHOTO: "+str(photo))
            status = sendphoto_hidekeyboard(message,message.chat_id(),None,open(photo,"rb"),caption=reply)
            logger.debug("ONESTREAMCOMMAND STATUS: "+str(status))
            if status == 400:
                hide_keyboard(message,message.chat_id(),reply)
            deleteconv(message)
    return _wrapper
