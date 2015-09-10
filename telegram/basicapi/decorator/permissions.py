__author__ = 'Tommy'

from telegram.tglogging import logger
from telegram.config.tgbotconfigparser import TGBotConfigParser

config = TGBotConfigParser("config.ini")
data = config.load()

def func_isadmin(message):
        user = message.from_User
        if str(user.chat_id) in data.get("basics", "superadmins"):
            logger.debug("@" + user.username + "(" + str(user.chat_id) + ") ist ein SuperAdmin.")
            return True
        else:
            logger.debug("@" + user.username + "(" + str(user.chat_id) + ") ist kein SuperAdmin")
            return False

def admin(func):
    def _isadmin(*args):
        message = args[1]
        if func_isadmin(message):
            func(*args)
    return _isadmin