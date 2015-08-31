# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'


import redis
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger
from telegram.basicapi.commands.messagecommands import MessageController

limitdb = 0
convdb = 1
limitserver = redis.StrictRedis(host="localhost",port="6379",db=limitdb)
convserver = redis.StrictRedis(host="localhost",port="6379",db=convdb)

config = TGBotConfigParser("config.ini")
configdata = config.load()

def getmessage(message):
    user = message.from_User
    return limitserver.get(str(user.chat_id))

def increasemessage(message):
    expire = configdata["basics"]["commandlimittime"]
    user = message.from_User

    pipe = limitserver.pipeline()
    pipe.get(str(user.chat_id))
    pipe.incr(str(user.chat_id))
    values = pipe.execute()
    if not values[0]:
        limitserver.expire(str(user.chat_id),expire)

    logger.debug("Response from Redis for key "+str(user.chat_id)+": "+ str(values))


def getuser_(message):
    userserver = redis.StrictRedis(db=convdb)
    userserver.hget("user-" + message.chat_id())

def commandAllowed(message):
    increasemessage(message)
    user = message.from_User
    limit = int(configdata["basics"]["commandlimit"])
    value = int(limitserver.get(str(user.chat_id)))
    if value>limit+1:
        logger.debug("User "+str(user.chat_id)+" hat sein Commandlimit von "+ str(limit) + " erreicht.")
        return False
    elif value == limit+1:
        expire = limitserver.ttl(str(user.chat_id))
        MessageController.sendreply(message, message.chat_id(),
                                    '''\U0000274E @%s, für dich sind die Commands erstmal für %s Sekunden blockiert.'''%(user.username,str(expire)))
    else:
        logger.debug("User "+str(user.chat_id)+" führt den  "+ str(value) + ". Command aus.")
        return True

