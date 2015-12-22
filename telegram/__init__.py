__author__ = 'Tommy'

from telegram.basicapi.model.message import Message
from telegram.tglogging import logger
from telegram.bot.parser import parsemessage



def activatebot(data):
    logger.debug("Message arrived.\nMessage: " + str(data))
    message = Message(data=data["message"])

    parsemessage(message)
