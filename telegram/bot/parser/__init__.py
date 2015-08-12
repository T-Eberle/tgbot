__author__ = 'Thomas'

from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.config.jsonconfigreader import JSONConfigReader
from telegram.tglogging import *

config = TGBotConfigParser("config.ini")
data = config.load()

jsongroups = JSONConfigReader("groups")

def isPermitted(message):
    if isAdmin(message) or isPermittedGroup(message):
        return True
    else:
        return False

def isAdmin(message):
    user = message.from_User
    if str(user.chat_id) in data.get("basics","superadmins"):
        logger.debug("@"+user.username+"("+str(user.chat_id)+") ist ein SuperAdmin.")
        return True
    else:
        return False
        logger.debug("@"+user.username+"("+str(user.chat_id)+") ist kein SuperAdmin")

def isPermittedGroup(message):
    jsongroups.read()
    jsondata = jsongroups.jsondata
    logger.debug("Is this a permitted group? "+str(message.chat_id()))
    logger.debug("Permitted Chat_Ids:"+str(jsondata.keys()))
    if str(message.chat_id()) in jsondata.keys():
        logger.debug("PERMITTED GROUP CHAT: "+ str(message.chat_id()))
        return True
    else:
        return False
