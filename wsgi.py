# -*- coding: utf-8 -*-
__author__ = 'Tommy'
import locale
import json

from uwsgidecorators import *
import telegram
from telegram.bot.timer import checkprimetime,checkuebergabe,gettracklist
from datetime import timedelta
from telegram.bot.decorators import *
import os
import shutil
from telegram.basicapi.wsgi import TGBotWSGI

configParser = TGBotConfigParser("config.ini")
config = configParser.load()

path = '/home/tgbot/telegrambot'
sys.path.append(path)
locale.setlocale(locale.LC_ALL, "de_DE.UTF8")


def application(environ,start_response):
    wsgi = TGBotWSGI(["users", "groups"])
    wsgi.application(environ,start_response)


@cron(10,-1,-1,-1,-1,target='spooler')
@db
def tracklist(num):
    gettracklist()


@cron(30, -1, -1, -1, -1, target='spooler')
@sleeping
@db
def primetime(num):
    checkprimetime()

@cron(40,-1,-1,-1,-1,target="spooler")
@db
def uebergabe(num):
    checkuebergabe()

@cron(0, -1, -1, -1, -1, target='spooler')
def backup(num):
    backup_path = config.get("json_files","json_path") + "/backups/"
    for dirpath,dirnames,filenames in os.walk(config.get("json_files","json_path")):
        for file in filenames:
            if dirpath == config.get("json_files","json_path"):
                curpath = os.path.join(dirpath,file)
                backup = os.path.join(backup_path,str(datetime.now().strftime("%y%m%d%H%M")) + file)
                shutil.copy(curpath,backup)
                logger.debug("Backup for file " + file + " created.")
            for file in filenames:
                curpath = os.path.join(dirpath, file)
                file_modified = datetime.fromtimestamp(os.path.getmtime(curpath))
            if datetime.now() - file_modified > timedelta(hours=24):
                os.remove(curpath)
                logger.debug("Backup " + file + " removed.")
