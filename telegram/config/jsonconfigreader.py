# -*- coding: utf-8 -*-
__author__ = 'Tommy'

import json

from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import *

class JSONConfigReader:
    def __init__(self, filename):
        config = TGBotConfigParser("config.ini")
        inidata = config.load()
        self.filename = filename
        self.data = inidata["json_files"]["json_path"]+"/"+filename+".json"
        self.jsondata = None


    def write(self,key,value):
        try:
            with open(self.data,"r") as f:
                self.jsondata = json.loads(f.read())
        except ValueError:
            self.jsondata = {}
        except FileNotFoundError:
            with open(self.data,"w+") as f:
                f.write("{}")
        finally:
            with open(self.data,"w") as f:
                self.jsondata[str(key)] = value
                self.dump(self.jsondata)

    def read(self):
        try:
            with open(self.data,"r") as f:
                f.seek(0)
                file = f.read()
                self.jsondata = json.loads(file)
                logger.debug("Reading file %s successful."% (self.filename))

        except ValueError as error:
            logger.exception(error)
            self.jsondata = {}

        except FileNotFoundError:
            with open(self.data,"w+") as f:
                f.write("{}")

    def dump(self,jsondata):
        with open(self.data, 'w') as f:
            f.write(json.dumps(jsondata))

    def delete(self,key):
        self.read()
        del self.jsondata[str(key)]
        self.dump(self.jsondata)

    def deleteall(self):
        self.read()
        self.dump({})

    def getValues(self,key):
        try:
            return self.jsondata[str(key)]
        except TypeError:
            return None
        except KeyError:
            return None
