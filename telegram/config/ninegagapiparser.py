# -*- coding: utf-8 -*-
__author__ = 'Carsten'

import requests
import random


class NineGagApiParser:
    @staticmethod
    def method():
        result = requests.get("http://api-9gag.herokuapp.com/")
        rand = random.randint(1,7)
        jsondata = result.json()
        return "[" + jsondata[rand]["title"] + "]" + "(" + jsondata[rand]["image"] + ")"
