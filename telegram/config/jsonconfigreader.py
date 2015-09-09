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
            if getfile(filename):
                logger.debug("Getting file "+filename+" from cache.")
                filedict = getfile(filename)
                dump = json.dumps(filedict)
                jsondata = json.loads(dump)
                setfile(filename,jsondata)
                logger.debug("Getting file "+filename+" was successful.")
            else:
                jsondata={}
                data = self.config["json_files"]["json_path"] + "/" + filename + ".json"
                try:
                    with open(data, encoding='utf-8',mode='r') as f:
                        logger.debug("Reading file %s." % filename)
                        file = f.read()
                        filedict= ast.literal_eval(file)
                        logger.debug("File content: "+file)
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
        file = getfile(filename)
        if file:
            with open(data, 'w') as f:
                f.write(json.dumps(file))

# if __name__=="__main__":
#     json_bytes = repr('''{"114978138": {"wao_id": "491333", "stream": "ht", "first_name": "\u00dcbergaben mit mir", "last_name": "bitte im IRC", "user_name": "maxwave"}, "76514156": {"wao_id": "367991", "stream": "tb hb ht ct", "first_name": "Hendrik \"Kirdneeez\"", "last_name": "Matz", "user_name": "Kirdneeez"}, "116358787": {"wao_id": "9", "first_name": "Alexander", "last_name": "Faustmann", "user_name": "Remolus1989"}, "115193377": {"wao_id": "151489", "stream": "ht", "first_name": "Denis", "last_name": "Eisenacher", "user_name": "Zhenos"}, "78113227": {"wao_id": "263019", "stream": "tb ht", "first_name": "Carsten", "last_name": "Bosner", "user_name": "Carreck"}, "111861557": {"wao_id": "4", "first_name": "Maik", "last_name": "V.-O.", "user_name": "michael_june"}, "54917518": {"wao_id": "271558", "first_name": "SEET", "last_name": "", "user_name": "unglaublicherSEET"}, "122089821": {"wao_id": "240757", "first_name": "Fabi", "last_name": "Ray-Fay", "user_name": "RayFay"}, "69209581": {"wao_id": "34119", "first_name": "Timo", "last_name": "Boldt", "user_name": "vibex"}, "118925656": {"wao_id": "525426", "first_name": "Mike", "last_name": "Sonic", "user_name": "MikeSonic"}, "96729362": {"wao_id": "474184", "stream": "ht", "first_name": "Fabse", "last_name": "", "user_name": "FabseHT"}, "7236920": {"wao_id": "518190", "first_name": "Danny", "last_name": "L", "user_name": "AULZZZzzzz"}, "111465322": {"wao_id": "452725", "stream": "ht", "first_name": "Michael 'Mike Rave'", "last_name": "Groth", "user_name": "MikeRave"}, "120111898": {"wao_id": "213201", "stream": "ht trb", "first_name": "Frontier", "last_name": "Sky", "user_name": "FrontierSky"}, "119801400": {"wao_id": "485878", "stream": "ht clt", "first_name": "Harm", "last_name": "Rosebrock", "user_name": "Korbito"}, "11548497": {"wao_id": "531080", "stream": "ht", "first_name": "Can", "last_name": "'B2Cee'", "user_name": "B2Cee"}, "68238135": {"wao_id": "528624", "first_name": "Tommy", "last_name": "Elroy", "user_name": "TommyElroy"}, "123521160": {"wao_id": "326686", "first_name": "Alex 'MadLex'", "last_name": "Behling", "user_name": "DJ_MadLex"}, "74057846": {"wao_id": "449960", "stream": "tb ht", "first_name": "Andreas", "last_name": "Wagner", "user_name": "AND_HT"}}(''')
#     # json_encoded = json_bytes.encode('raw_unicode_string')
#     result = json.dumps(ast.literal_eval(json_bytes))
#     print(result)
#     data = json.load(result)
#
#     print(str(data))