__author__ = 'Thomas Eberle'

import redis
from telegram.bot.tglogging.TGLogger import logger

userdb = 0
convdb = 1
convserver = redis.StrictRedis(host="localhost",port="6379",db=userdb)
userserver = redis.StrictRedis(host="localhost",port="6379",db=convdb)


class TGRedisHandler:
    @staticmethod
    def setuser(message, waoid="528624"):
        user = message.from_User
        userserver.set("user-" + str(message.chat_id()),waoid)
        logger.debug("DB-Entry user-" + message.chat_id() + " added!")

    @staticmethod
    def getuser_(message):
        userserver = redis.StrictRedis(db=convdb)
        userserver.hget("user-" + message.chat_id())
