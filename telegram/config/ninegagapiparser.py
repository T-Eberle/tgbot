# -*- coding: utf-8 -*-
__author__ = 'Carsten'

import requests
import random


class NineGagApiParser:
    @staticmethod
    def method():
        result = requests.get("http://api-9gag.herokuapp.com/")
        jsondata = result.json()
        size_result = len(jsondata)
        rand = random.randint(0,size_result - 1)
        return "[" + jsondata[rand]["title"] + "]" + "(" + jsondata[rand]["image"] + ")"
