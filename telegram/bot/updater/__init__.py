__author__ = 'Tommy'


from telegram.config.jsonconfigreader import JSONConfigReader
from telegram.tglogging import logger


jsonusers = JSONConfigReader("users")
jsongroups = JSONConfigReader("groups")


def updateuser(user):
    jsonusers.read()
    try:
        if jsonusers.getValues(user.chat_id):
            oldValues = jsonusers.getValues(user.chat_id).copy()
            values = jsonusers.getValues(user.chat_id)
            if values != oldValues:
                logger.debug("User has changed!")
                jsonusers.write(user.chat_id,values)
    except KeyError as error:
        pass

def updategroup(message):
    jsongroups.read()
    try:
        if jsongroups.getValues(message.chat_id()) and message.new_chat_title:
            jsongroups.write(message.chat_id(),message.new_chat_title)
            logger.debug("Groupname has changed!")
    except KeyError as error:
        pass