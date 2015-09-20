# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import requests
import pkg_resources
from telegram.tglogging import *


class HTTPRequestController:
    def __init__(self, url=None, values=None):
        self.url = url
        self.values = values

    @staticmethod
    def requestwithvaluesxwwwurlencoded(url, values):
        req = requests.post(url,params=values)
        logger.debug("URL: " + str(req.url))
        return req.raise_for_status()

    @staticmethod
    def requestwithfile(url, values,file_id,file,filename=None):
        if not filename:
            files = {file_id: file}
        else:
            files = {file_id: (filename, file)}
        html = requests.post(url,params=values,files=files)
        logger.debug("URL: " + str(html.text))

    @staticmethod
    def requestwithdata(url,values,data):
        html = requests.post(url,params=values,data=data)
        logger.debug("URL: " + str(html.text))
