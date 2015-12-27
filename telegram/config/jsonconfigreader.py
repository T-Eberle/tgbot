# -*- coding: utf-8 -*-
__author__ = 'Tommy'

from telegram.tgredis import TGRedis
from telegram.tglogging import *
import json
import ast


class JSONConfigReader:
    def __init__(self, filenames, jsonconfig):
        self.filenames = filenames
        self.config = jsonconfig

    def createcacheforfiles(self):
        """
        Lädt alle angegebenen Dateien vom JSON-Dateiordner in Redis.
        """
        for filename in self.filenames:
            if TGRedis.getfile(filename):
                logger.debug("Getting file " + filename + " from cache.")
                filedict = TGRedis.getfile(filename)
                dump = json.dumps(filedict)
                jsondata = json.loads(dump)
                TGRedis.setfile(filename,jsondata)
                logger.debug("Getting file " + filename + " was successful.")
            else:
                jsondata = {}
                data = self.config["json_files"]["json_path"] + "/" + filename + ".json"
                try:
                    with open(data, encoding='utf-8',mode='r') as f:
                        logger.debug("Reading file %s." % filename)
                        file = f.read()
                        filedict = ast.literal_eval(file)
                        logger.debug("File content: " + file)
                        jsondump = json.dumps(filedict)
                        jsondata = json.loads(jsondump)
                        logger.debug("Reading file %s successful." % filename)

                except ValueError as error:
                    logger.exception(error)
                    with open(data, "w+") as f:
                        f.write("{}")
                    jsondata = {}

                except FileNotFoundError as error:
                    logger.exception(error)
                    with open(data, "w+") as f:
                        f.write("{}")
                    jsondata = {}
                finally:
                    TGRedis.setfile(filename, jsondata)

    def savecachetofiles(self):
        """
        Speichert den Wert aus Redis in die Dateien.
        Danach wird die komplette Datei-Datenbank von Redis gelöscht.
        """
        logger.debug("FILENAMES: "+str(self.filenames))
        for filename in self.filenames:
            data = self.config["json_files"]["json_path"] + "/" + filename + ".json"
            self.dump(data, filename)

    @staticmethod
    def dump(data, filename):
        file = TGRedis.getfile(filename)
        if file:
            with open(data, 'w') as f:
                f.write(json.dumps(file))
