# -*- coding: utf-8 -*-
__author__ = 'Tommy'
import sys
import locale
import json
from uwsgidecorators import *
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import *
from telegram.bot.timer import *
from telegram.config.jsonconfigreader import JSONConfigReader



from telegram import activateBot

configParser = TGBotConfigParser("config.ini")
config = configParser.load()
files = ["users","groups"]
filereader = JSONConfigReader(files,config)

path = '/home/tgbot/telegrambot'
sys.path.append(path)
locale.setlocale(locale.LC_ALL,"de_DE.UTF8")

def application(environ,start_response):
    filereader.createCacheForFiles()
    start_response('200 OK',[('Content-Type','text/html')])

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    if request_body_size != 0:
        request_body = environ['wsgi.input'].read(request_body_size)
        obj = json.loads(request_body.decode('utf-8'))
        activateBot(obj)
    filereader.saveCacheToFiles()
    return b''


#TODO Timer für getimte Events: Check Ticket #81
@cron(int(config.get("basics","time_interval")), -1, -1, -1, -1,target='spooler')
def execute_me_every_x_min(num):
    filereader.createCacheForFiles()
    if not(int(config.get("basics","sleep_start")) <= datetime.now().hour < int(config.get("basics","sleep_end"))):
        logger.debug(config.get("basics","time_interval")+" minutes, what a long time!")
        checkPrimetime()
    filereader.saveCacheToFiles()