__author__ = 'Thomas Eberle'

from telegram.basicapi.model.message import Message
from telegram.basicapi.model.inlineQuery import InlineQuery
from telegram.tglogging import logger
from telegram.basicapi.parser import parsemessage,parseinline

def activatebot(data,wartungsmodus,commands,inlinecommands):
    logger.debug("Message arrived.\nMessage: " + str(data))
    if "message" in data:
        message = Message(data=data["message"])
        parsemessage(message,wartungsmodus,commands)
    elif "inline_query" in data:
        inline = InlineQuery(data=data["inline_query"])
        parseinline(inline,inlinecommands)
        logger.debug("IN INLINE QUERY")
