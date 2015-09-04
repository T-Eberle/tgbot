__author__ = 'Tommy'


from telegram.config.jsonconfigreader import JSONConfigReader
from telegram.tglogging import logger
from telegram.tgredis import setfile,getfile

def updateuser(user):
    jsonusers = getfile("users")
    try:
        if jsonusers[user.chat_id]:
            oldValues = jsonusers[user.chat_id].copy()
            values = jsonusers[user.chat_id]
            values["first_name"]= user.first_name
            values["user_name"]= user.username
            values["last_name"]= user.last_name
            if values != oldValues:
                logger.debug("User has changed!")
                jsonusers[str(user.chat_id)] = values
                setfile("users",jsonusers)
    except KeyError as error:
        pass

def updategroup(message):
    jsongroups = getfile("groups")
    try:
        logger.debug(str(jsongroups))
        if jsongroups and message.new_chat_title:
            jsongroups[message.chat_id()] = message.new_chat_title
            setfile("groups",jsongroups)
            logger.debug("Groupname has changed!")
    except KeyError as error:
        pass
