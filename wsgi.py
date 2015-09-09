# -*- coding: utf-8 -*-
__author__ = 'Tommy'
import locale
import json

from uwsgidecorators import *
from os import listdir
from os.path import isfile, join
from telegram.bot.timer import *
from telegram.config.jsonconfigreader import JSONConfigReader
from telegram import activatebot
from datetime import timedelta
import uwsgi
import shutil

configParser = TGBotConfigParser("config.ini")
config = configParser.load()
files = ["users", "groups"]
filereader = JSONConfigReader(files, config)

path = '/home/tgbot/telegrambot'
sys.path.append(path)
locale.setlocale(locale.LC_ALL, "de_DE.UTF8")


def application(environ, start_response):
    uwsgi.signal(13)
    start_response('200 OK', [('Content-Type', 'text/html')])

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    if request_body_size != 0:
        request_body = environ['wsgi.input'].read(request_body_size)
        obj = json.loads(request_body.decode('utf-8'))
        activatebot(obj)
    uwsgi.signal(14)
    return b''

@lock
@signal(13)
def loadfromfile(num):
    logger.info("LOAD FILES.")
    filereader.createcacheforfiles()

@lock
@signal(14)
def savetofile(num):
    logger.info("SAVING FILES.")
    filereader.savecachetofiles()


# TODO Timer für getimte Events: Check Ticket #81
@cron(int(config.get("basics", "time_interval")), -1, -1, -1, -1, target='spooler')
def primetime(num):
    uwsgi.signal(13)
    if not (int(config.get("basics", "sleep_start")) <= datetime.now().hour < int(config.get("basics", "sleep_end"))):
        logger.debug(config.get("basics", "time_interval") + " minutes, what a long time!")
        checkprimetime()
    uwsgi.signal(14)

@cron(0, -1, -1, -1, -1, target='spooler')
def backup(num):
   backup_path = config.get("json_files","json_path")+"/backups/"
   for dirpath,dirnames,filenames in os.walk(config.get("json_files","json_path")):
       for file in filenames:
           if dirpath == config.get("json_files","json_path"):
               curpath = os.path.join(dirpath,file)
               backup = os.path.join(backup_path,str(datetime.now().strftime("%y%m%d%H%M"))+file)
               shutil.copy(curpath,backup)
               logger.debug("Backup " + file + " created.")
       for file in filenames:
          curpath = os.path.join(dirpath, file)
          file_modified = datetime.fromtimestamp(os.path.getmtime(curpath))
          if datetime.now() - file_modified > timedelta(hours=24):
              os.remove(curpath)
              logger.debug("Backup " + file + " removed.")