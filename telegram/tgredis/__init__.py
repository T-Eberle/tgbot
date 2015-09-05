# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import ast

import redis

from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger
from telegram.basicapi.commands.messagecommands import MessageController
from resources import emoji

limitdb = 0
convdb = 1
filedb = 2
limitserver = redis.StrictRedis(host="localhost", port="6379", db=limitdb)
convserver = redis.StrictRedis(host="localhost", port="6379", db=convdb)
fileserver = redis.StrictRedis(host="localhost", port="6379", db=filedb)

config = TGBotConfigParser("config.ini")
configdata = config.load()


def setfile(filename, jsonfile):
    logger.debug("SET FILE: " + str(jsonfile))
    fileserver.set(filename, jsonfile)


def getfile(filename):
    data = {}
    try:
        file = fileserver.get(filename)
        if file:
            data = ast.literal_eval(file.decode("utf-8"))
    except redis.exceptions.ResponseError:
        logger.debug("REDIS: Couldn't find " + filename)
    return data


def setfilevalue(filename, key, value):
    data = getfile(filename)
    data[str(key)] = value
    setfile(filename, data)


def getfilevalue(filename, key):
    try:
        data = getfile(filename)
        result = data[str(key)]
    except KeyError:
        result = None
    return result


def deleteentryfromfile(filename, key):
    data = getfile(filename)
    del data[str(key)]
    setfile(filename, data)


def flushallfiles():
    fileserver.flushdb()


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
        limitserver.expire(str(user.chat_id), expire)

    logger.debug("Response from Redis for key " + str(user.chat_id) + ": " + str(values))


def commandallowed(message):
    increasemessage(message)
    user = message.from_User
    limit = int(configdata["basics"]["commandlimit"])
    value = int(limitserver.get(str(user.chat_id)))
    if value > limit + 1:
        logger.debug("User " + str(user.chat_id) + " hat sein Commandlimit von " + str(limit) + " erreicht.")
        return False
    elif value == limit + 1:
        expire = limitserver.ttl(str(user.chat_id))
        MessageController.sendreply(message, message.chat_id(),
                                    '''%s @%s, für dich sind die Commands erstmal für %s Sekunden blockiert.'''
                                    % (emoji.cross_mark,user.username, str(expire)))
    else:
        logger.debug("User " + str(user.chat_id) + " führt den  " + str(value) + ". Command aus.")
        return True
