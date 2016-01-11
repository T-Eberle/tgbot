# -*- coding: utf-8 -*-
__author__ = 'Carsten'

import requests
import random
import re
from tgbot.tglogging import logger

class NineGagApiParser:

    @staticmethod
    def ninegag(type=""):
        result = requests.get("http://infinigag.eu01.aws.af.cm/"+type)
        jsondata = result.json()
        size_result = len(jsondata["data"])
        rand = random.randint(0,size_result - 1)
        result = jsondata["data"][rand]["caption"], jsondata["data"][rand]["images"]["large"]
        return result

    @staticmethod
    def pr0gramm():
        result = requests.get("http://pr0gramm.com/api/items/get")
        jsondata = result.json()
        size_result = len(jsondata)
        i = 0
        for element in jsondata["items"]:
            if "webm" in jsondata["items"][i]["image"]:
                del(jsondata["items"][i])
            else:
                i += 1
        rand = random.randint(0,size_result - 1)
        result = "http://img.pr0gramm.com/" + jsondata["items"][rand]["image"]
        return result

    @staticmethod
    def xkcd():
        result = requests.get("http://xkcd.com/info.0.json")
        jsondata = result.json()
        number = jsondata["num"]
        rand = random.randint(1,number)
        result = requests.get("http://xkcd.com/"+str(rand)+"/info.0.json")
        jsondata = result.json()
        return jsondata
