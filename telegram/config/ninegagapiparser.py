# -*- coding: utf-8 -*-
__author__ = 'Carsten'

import requests
import random


class NineGagApiParser:
    @staticmethod
    def method():
        result = requests.get("http://api-9gag.herokuapp.com/")
        size_result = len(result)
        rand = random.randint(0,size_result - 1)
        jsondata = result.json()
        return "[" + jsondata[rand]["title"] + "]" + "(" + jsondata[rand]["image"] + ")"
