__author__ = 'Thomas Eberle'

from tgbot.basicapi.model.message import Message
from tgbot.basicapi.model.inlineQuery import InlineQuery
from tgbot.tglogging import logger
from tgbot.basicapi.parser import parsemessage,parseinline
import tgbot


def activatebot(data,wartungsmodus,commands,inlinecommands):
    logger.debug("Message arrived.\nMessage: " + str(data))
    if "message" in data:
        message = Message(data=data["message"])
        tgbot.mainmessage = message
        parsemessage(message,commands,wartungsmodus)
    elif "inline_query" in data:
        inline = InlineQuery(data=data["inline_query"])
        parseinline(inline,inlinecommands)
        logger.debug("IN INLINE QUERY")
