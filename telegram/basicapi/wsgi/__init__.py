__author__ = 'Tommy'

from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.config.jsonconfigreader import JSONConfigReader
import telegram
import json

class TGBotWSGI:

    def setFiles(self,files):
        self.files = files

    def getFiles(self):
        return self.files

    def __init__(self,files):
        self.setFiles(files)

    def application(self,environ, start_response):
        files = self.getFiles()
        self.configParser = TGBotConfigParser("config.ini")
        self.config = self.configParser.load()
        filereader = JSONConfigReader(files, self.config)
        filereader.createcacheforfiles()
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

