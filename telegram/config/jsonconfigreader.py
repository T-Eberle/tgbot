# -*- coding: utf-8 -*-
__author__ = 'Tommy'

import json

from telegram.tgredis import *
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import *


class JSONConfigReader:


    def __init__(self,filenames,config):
        self.filenames = filenames
        self.config = config

    def createCacheForFiles(self):
        for filename in self.filenames:
             jsondata = {}
             data = self.config["json_files"]["json_path"]+"/"+filename+".json"
             try:
                with open(data,"r") as f:
                    f.seek(0)
                    file = f.read()
                    logger.debug("Reading file %s."% (filename))
                    jsondata = json.loads(file)
                    logger.debug("Reading file %s successful."% (filename))

             except ValueError as error:
                logger.exception(error)
                with open(data,"w+") as f:
                    f.write("{}")
                jsondata = {}

             except FileNotFoundError:
                with open(data,"w+") as f:
                    f.write("{}")
                jsondata = {}
             finally:
                setfile(filename,jsondata)

    def saveCacheToFiles(self):
        for filename in self.filenames:
            data = self.config["json_files"]["json_path"]+"/"+filename+".json"
            self.dump(data,filename)
        flushallfiles()

    def dump(self,data,filename):
        with open(data, 'w') as f:
            f.write(json.dumps(getfile(filename)))

