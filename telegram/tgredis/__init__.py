# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import ast

import redis

from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger

limitdb = 0
convdb = 1
filedb = 2
limitserver = redis.StrictRedis(host="localhost", port="6379", db=limitdb)
convserver = redis.StrictRedis(host="localhost", port="6379", db=convdb)
fileserver = redis.StrictRedis(host="localhost", port="6379", db=filedb)

config = TGBotConfigParser("config.ini")
configdata = config.load()


def addtoconv(message,value):
    pass
    # user = message.from_User
    # new_value = ""
    # conv = getconv(message)
    # if conv != "None":
    #     new_value += conv + " ; "
    # new_value += value
    # pipe = convserver.pipeline()
    # pipe.set(user.chat_id,new_value)
    # pipe.expire(user.chat_id,120)
    # pipe.execute()


def setconvcommand(message,value):
    user = message.from_User
    pipe = convserver.pipeline()
    pipe.hset(user.chat_id,"command",value)
    pipe.expire(user.chat_id,120)
    pipe.execute()


def getconvcommand(message):
    user = message.from_User
    result = convserver.hget(user.chat_id,"command")
    if result:
        return result.decode("utf-8")
    else:
        return result


def setconvkey(message,key,value):
    user = message.from_User
    pipe = convserver.pipeline()
    pipe.hset(user.chat_id,key,value)
    pipe.expire(user.chat_id,120)
    pipe.execute()


def getconvkey(message,key):
    user = message.from_User
    return str(convserver.hget(user.chat_id,key))


def getconv(message):
    user = message.from_User
    return str(convserver.get(user.chat_id))


def deleteconv(message):
    user = message.from_User
    convserver.delete(user.chat_id)


def setfile(filename, jsonfile):
    logger.debug("SET FILE: " + str(jsonfile))
    pipe = fileserver.pipeline()
    pipe.set(filename, jsonfile)
    pipe.expire(filename,int(configdata["json_files"]["file_expire"]))
    pipe.execute()


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
