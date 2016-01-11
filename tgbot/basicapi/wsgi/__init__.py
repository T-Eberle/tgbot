__author__ = 'Tommy'

from tgbot.config.tgbotconfigparser import TGBotConfigParser
from tgbot.config.jsonconfigreader import JSONConfigReader
from tgbot.tgredis import TGRedis
from tgbot.basicapi import activatebot
import json
from tgbot.tglogging import logger
import tgbot

class TGBotWSGI:
    def setFiles(self,files):
        self.files = files

    def getFiles(self):
        return self.files

    def __init__(self,files,wartungsmodus,commandclasses,inlineclasses=None,redis_limitserver=0,redis_convserver=1,redis_fileserver=2,configfile="basicconfig.ini",configpath="tgbot.resources.config"):
        self.redis_convserver = redis_convserver
        self.redis_fileserver = redis_fileserver
        self.redis_limitserver = redis_limitserver
        self.tgredis = TGRedis(redis_limitserver,redis_convserver,redis_fileserver)
        self.setFiles(files)
        self.wartungsmodus = wartungsmodus
        self.commandclasses = commandclasses
        self.inlineclasses = inlineclasses
        self.configfile = configfile
        self.configpath = configpath
        self.configParser = TGBotConfigParser(self.configfile,self.configpath)
        tgbot.iniconfig = self.configParser.load()
        logger.debug("CONFIG: "+str(tgbot.iniconfig))

    def application(self,environ, start_response):
        tgbot.iniconfig = self.configParser.load()
        logger.debug("CONFIG: "+str(tgbot.iniconfig))
        logger.debug("ENVIRON: "+str(environ))
        logger.debug("START_RESPONSE: "+str(start_response))
        #while True:
        files = self.getFiles()
        self.filereader = JSONConfigReader(files)
        self.filereader.createcacheforfiles()
        start_response('200 OK', [('Content-Type', 'text/html')])
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0

        if request_body_size != 0:
            request_body = environ['wsgi.input'].read(request_body_size)
            obj = json.loads(request_body.decode('utf-8'))
            activatebot(obj,self.wartungsmodus,self.commandclasses,self.inlineclasses)
        self.filereader.savecachetofiles()

        return b''

