__author__ = 'Thomas Eberle'

from telegram.basicapi.model.message import Message
from telegram.tglogging import logger
from telegram.basicapi.parser import parsemessage

def activatebot(data,wartungsmodus,args):
    logger.debug("Message arrived.\nMessage: " + str(data))
    message = Message(data=data["message"])

    parsemessage(message,wartungsmodus,args)
