# -*- coding: utf-8 -*-
__author__ = 'Tommy'

from telegram.config.jsonconfigreader import JSONConfigReader
from datetime import datetime
from telegram.tgredis import *
from telegram.basicapi.commands import sendreply


configParser = TGBotConfigParser("config.ini")
config = configParser.load()
files = ["users", "groups"]
filereader = JSONConfigReader(files, config)


def limited(func):
    def _limited(*args):
        logger.debug("ARGS: " + str(args))
        message = args[1]
        increasemessage(message)
        user = message.from_User
        limit = int(configdata["basics"]["commandlimit"])
        value = int(limitserver.get(str(user.chat_id)))
        if value > limit + 1:
            logger.debug("User " + str(user.chat_id) + " hat sein Commandlimit von " + str(limit) + " erreicht.")
            return
        elif value == limit + 1:
            expire = limitserver.ttl(str(user.chat_id))
            sendreply(message, message.chat_id(),
                                        '''%s @%s, für dich sind die Commands erstmal für %s Sekunden blockiert.'''
                                        % (emoji.cross_mark,user.username, str(expire)))
            return
        else:
            logger.debug("User " + str(user.chat_id) + " führt den  " + str(value) + ". Command aus.")
            func(*args)
    return _limited


def sleeping(func):
    def _sleeping(*args):
        if not (int(config.get("basics", "sleep_start")) <= datetime.now().hour < int(config.get("basics",
                                                                                                 "sleep_end"))):
            logger.debug("IN ACTIVE MODE")
            func(*args)
        else:
            logger.debug("IN SLEEPING MODE")
    return _sleeping


def db(func):
    def _db(*args):
        createcache()
        func(args)
        savecache()
    return _db


def createcache():
    logger.info("LOAD FILES.")
    filereader.createcacheforfiles()


def savecache():
    logger.info("SAVING FILES.")
    filereader.savecachetofiles()
