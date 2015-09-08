# -*- coding: utf-8 -*-
__author__ = 'Tommy'

from telegram.tgredis import *
from telegram.tglogging import *
import json


class JSONConfigReader:
    def __init__(self, filenames, jsonconfig):
        self.filenames = filenames
        self.config = jsonconfig

    def createcacheforfiles(self):
        """
        Lädt alle angegebenen Dateien vom JSON-Dateiordner in Redis.
        """
        for filename in self.filenames:
            jsondata = {}
            data = self.config["json_files"]["json_path"] + "/" + filename + ".json"
            try:
                with open(data, "r") as f:
                    f.seek(0)
                    file = f.read()
                    logger.debug("Reading file %s." % filename)
                    jsondata = json.loads(file)
                    logger.debug("Reading file %s successful." % filename)

            except ValueError as error:
                logger.exception(error)
                with open(data, "w+") as f:
                    f.write("{}")
                jsondata = {}

            except FileNotFoundError:
                with open(data, "w+") as f:
                    f.write("{}")
                jsondata = {}
            finally:
                setfile(filename, jsondata)

    def savecachetofiles(self):
        """
        Speichert den Wert aus Redis in die Dateien.
        Danach wird die komplette Datei-Datenbank von Redis gelöscht.
        """
        for filename in self.filenames:
            data = self.config["json_files"]["json_path"] + "/" + filename + ".json"
            self.dump(data, filename)

    @staticmethod
    def dump(data, filename):
        with open(data, 'w') as f:
            f.write(json.dumps(getfile(filename)))
