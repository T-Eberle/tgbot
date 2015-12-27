__author__ = 'Tommy'

from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.config.jsonconfigreader import JSONConfigReader
from telegram.tgredis import TGRedis
import telegram
import json
from telegram.tglogging import logger

class TGBotWSGI:

    def setFiles(self,files):
        self.files = files

    def getFiles(self):
        return self.files

    def __init__(self,files,redis_limitserver=0,redis_convserver=1,redis_fileserver=2):
        self.redis_convserver = redis_convserver
        self.redis_fileserver = redis_fileserver
        self.redis_limitserver = redis_limitserver
        self.tgredis= TGRedis(redis_limitserver,redis_convserver,redis_fileserver)
        self.setFiles(files)

    def application(self,environ, start_response):
        logger.debug("ENVIRON: "+str(environ))
        logger.debug("START_RESPONSE: "+str(start_response))
        #while True:
        files = self.getFiles()
        self.configParser = TGBotConfigParser("config.ini")
        self.config = self.configParser.load()
        self.filereader = JSONConfigReader(files, self.config)
        self.filereader.createcacheforfiles()
        start_response('200 OK', [('Content-Type', 'text/html')])
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0

        if request_body_size != 0:
            request_body = environ['wsgi.input'].read(request_body_size)
            obj = json.loads(request_body.decode('utf-8'))
            telegram.activatebot(obj)
        self.filereader.savecachetofiles()

        return b''

