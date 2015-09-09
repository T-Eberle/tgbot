__author__ = 'Tommy'

from telegram.tglogging import logger
from telegram.tgredis import setfile, getfile,setfilevalue


def updateuser(user):
    jsonusers = getfile("users")
    logger.debug("User ID: "+str(user.chat_id))
    try:
        if jsonusers[str(user.chat_id)]:
            oldvalues = jsonusers[str(user.chat_id)].copy()
            values = jsonusers[str(user.chat_id)]
            values["first_name"] = user.first_name
            values["user_name"] = user.username
            values["last_name"] = user.last_name
            if values != oldvalues:
                logger.debug("User has changed!")
                setfilevalue("users",user.chat_id, values)
    except KeyError:
        logger.error("Updater: Can't get user?!")


def updategroup(message):
    jsongroups = getfile("groups")
    try:
        logger.debug(str(jsongroups))
        if jsongroups and message.new_chat_title:
            jsongroups[message.chat_id()] = message.new_chat_title
            setfile("groups", jsongroups)
            logger.debug("Groupname has changed!")
    except KeyError:
        logger.error("Updater: Can't get group?!")
