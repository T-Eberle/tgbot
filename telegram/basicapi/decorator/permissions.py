# -*- coding: utf-8 -*-
__author__ = 'Tommy'

from telegram.tglogging import logger
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tgredis import getfile,getfilevalue
from telegram.basicapi.commands import sendreply
from resources import emoji

config = TGBotConfigParser("config.ini")
data = config.load()


def grouptype(*params):
    def _grouptype(func):
        def _wrapped(*args):
            message = args[1]
            if correctgrouptype(message.chat_id(),*params):
                func(*args)
                return
        return _wrapped
    return _grouptype


def correctgrouptype(chat_id,*params):
    values = getfilevalue("groups",chat_id)
    if not values:
        return True
    else:
        type = values.get("type")
        if not type:
            return True
        for param in params:
            if param in type:
                return True
    return False

def func_ispermitteduser(message):
    users = getfile("users")
    logger.debug("Is this a permitted user? " + str(message.chat_id()))
    logger.debug("Permitted Chat_Ids:" + str(users.keys()))
    user = message.chat_id()
    if str(user) in users.keys():
        logger.debug("USER PERMITTED: " + str(user))
        return True
    else:
        return False


def func_ispermittedgroup(message):
    groups = getfile("groups")
    logger.debug("Is this a permitted group? " + str(message.chat_id()))
    logger.debug("Permitted Chat_Ids:" + str(groups.keys()))
    if str(message.chat_id()) in groups.keys():
        logger.debug("PERMITTED GROUP CHAT: " + str(message.chat_id()))
        return True
    else:
        return False


def func_ispermitted(message):
    if func_isadmin(message):
        return True
    elif func_ispermittedgroup(message):
        return True
    elif func_ispermitteduser(message):
        return True
    else:
        return False


def func_isadmin(message):
        user = message.from_User
        if str(user.chat_id) in data.get("basics", "superadmins"):
            logger.debug("@" + user.username + "(" + str(user.chat_id) + ") ist ein SuperAdmin.")
            return True
        else:
            logger.debug("@" + user.username + "(" + str(user.chat_id) + ") ist kein SuperAdmin")
            return False

def group_only(func):
    def _group_only(*args):
        message = args[1]
        if func_ispermittedgroup(message):
            func(*args)
        else:
            logger.warn("User not allowed to communicate with Bot.")
    return _group_only

def registered_only(func):
    def _registered_only(*args):
        message = args[1]
        if func_ispermittedgroup(message):
            func(*args)
        else:
            logger.warn("User not allowed to communicate with Bot.")
    return _registered_only


def permitted(func):

    def _permitted(*args):
        message = args[1]
        if func_ispermitted(message):
            func(*args)
        else:
            logger.warn("User not allowed to communicate with Bot.")
    return _permitted


def admin(func):
    def _isadmin(*args):
        message = args[1]
        if func_isadmin(message):
            func(*args)
    return _isadmin


def botonly(botfunc):
    def _botonly(*args):
        message = args[1]
        user = message.from_User
        user_id = user.chat_id
        if message.chat_id() != user_id:
            sendreply(message,message.chat_id(),emoji.warning +
                                        user.first_name +
                                        ", diesen Befehl kannst du nur im Chat des Bots ausführen! @waobot" +
                                        emoji.warning)
        else:
            botfunc(*args)

    return _botonly