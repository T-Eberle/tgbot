# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import ast

import redis

from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger

class TGRedis:

    limitserver = redis.StrictRedis(host="localhost", port="6379", db=0)
    convserver = redis.StrictRedis(host="localhost", port="6379", db=1,decode_responses=True)
    fileserver = redis.StrictRedis(host="localhost", port="6379", db=2)
    convserver.set_response_callback("HGET",str)
    config = TGBotConfigParser("config.ini")
    configdata = config.load()

    def __init__(self,limitdb=0,convdb=1,filedb=2):
        if limitdb == convdb or limitdb == filedb or convdb==filedb:
            return
        self.limitdb = limitdb
        self.convdb = convdb
        self.filedb = filedb
        TGRedis.limitserver = redis.StrictRedis(host="localhost", port="6379", db=limitdb)
        TGRedis.convserver = redis.StrictRedis(host="localhost", port="6379", db=convdb,decode_responses=True)
        TGRedis.fileserver = redis.StrictRedis(host="localhost", port="6379", db=filedb)
        TGRedis.convserver.set_response_callback("HGET",str)


    def addtoconv(self,message,value):
        pass

    @staticmethod
    def setconvcommand(message,value):
        user = message.from_User
        pipe = TGRedis.convserver.pipeline()
        pipe.hset(user.chat_id,"command",value)
        pipe.expire(user.chat_id,120)
        pipe.execute()

    @staticmethod
    def getconvcommand(self,message):
        user = message.from_User
        result = self.convserver.hget(user.chat_id,"command")
        if result:
            return str(result)
        else:
            return result

    @staticmethod
    def setconvkey(message,key,value):
        user = message.from_User
        pipe = TGRedis.convserver.pipeline()
        pipe.hset(user.chat_id,key,value)
        pipe.expire(user.chat_id,120)
        pipe.execute()

    @staticmethod
    def getconvkey(message,key):
        user = message.from_User
        return TGRedis.convserver.hget(user.chat_id,key)

    @staticmethod
    def getconv(message):
        user = message.from_User
        return str(TGRedis.convserver.get(user.chat_id))

    @staticmethod
    def deleteconv(message):
        user = message.from_User
        TGRedis.convserver.delete(user.chat_id)

    @staticmethod
    def setfile(filename, jsonfile):
        logger.debug("SET FILE: " + str(jsonfile))
        pipe = TGRedis.fileserver.pipeline()
        pipe.set(filename, jsonfile)
        pipe.expire(filename,int(TGRedis.configdata["json_files"]["file_expire"]))
        pipe.execute()

    @staticmethod
    def getfile(filename):
        data = {}
        try:
            file = TGRedis.fileserver.get(filename)
            if file:
                data = ast.literal_eval(file.decode("utf-8"))
        except redis.exceptions.ResponseError:
            logger.debug("REDIS: Couldn't find " + filename)
        return data

    @staticmethod
    def setfilevalue(filename, key, value):
        data = TGRedis.getfile(filename)
        data[str(key)] = value
        TGRedis.setfile(filename, data)

    @staticmethod
    def getfilevalue(filename, key):
        try:
            data = TGRedis.getfile(filename)
            result = data[str(key)]
        except KeyError:
            result = None
        return result

    @staticmethod
    def deleteentryfromfile(filename, key):
        data = TGRedis.getfile(filename)
        del data[str(key)]
        TGRedis.setfile(filename, data)

    @staticmethod
    def flushallfiles():
        TGRedis.fileserver.flushdb()

    @staticmethod
    def getmessage(message):
        user = message.from_User
        return TGRedis.limitserver.get(str(user.chat_id))

    @staticmethod
    def increasemessage(message):
        expire = TGRedis.configdata["basics"]["commandlimittime"]
        user = message.from_User
        limit_id = str(user.chat_id)+"/"+str(message.chat_id())
        pipe = TGRedis.limitserver.pipeline()
        pipe.get(limit_id)
        pipe.incr(limit_id)
        values = pipe.execute()
        if not values[0]:
            TGRedis.limitserver.expire(limit_id, expire)

        logger.debug("Response from Redis for key " + limit_id + ": " + str(values))
