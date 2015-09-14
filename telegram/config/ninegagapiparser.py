# -*- coding: utf-8 -*-
__author__ = 'Carsten'

import requests
import random


class NineGagApiParser:
    @staticmethod
    def ninegag():
        result = requests.get("http://api-9gag.herokuapp.com/")
        jsondata = result.json()
        size_result = len(jsondata)
        rand = random.randint(0,size_result - 1)
        return "[" + jsondata[rand]["title"] + "]" + "(" + jsondata[rand]["image"] + ")"

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
        return "http://img.pr0gramm.com/" + jsondata["items"][rand]["image"]

if __name__ == "__main__":
    NineGagApiParser.pr0gramm()
