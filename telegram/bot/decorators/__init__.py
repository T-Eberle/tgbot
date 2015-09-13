__author__ = 'Tommy'

from telegram.config.jsonconfigreader import JSONConfigReader
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger
from datetime import datetime


configParser = TGBotConfigParser("config.ini")
config = configParser.load()
files = ["users", "groups"]
filereader = JSONConfigReader(files, config)


def sleeping(func):
    def _sleeping(*args):
        if not (int(config.get("basics", "sleep_start")) <= datetime.now().hour < int(config.get("basics", "sleep_end"))):
            logger.debug("IN ACTIVE MODE")
            func(*args)
        else:
            logger.debug("IN SLEEPING MODE")
    return _sleeping

def db (func):
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

