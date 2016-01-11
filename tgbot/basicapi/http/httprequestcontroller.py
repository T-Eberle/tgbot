# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import requests
import pkg_resources
from tgbot.tglogging import *


class HTTPRequestController:
    def __init__(self, url=None, values=None):
        self.url = url
        self.values = values

    @staticmethod
    def requestwithvaluesxwwwurlencoded(url, values):
        req = requests.post(url,params=values)
        logger.debug("URL: " + str(req.url))
        logger.debug("ANSWER FROM REQUEST: "+ str(req.content))
        return req.json()

    @staticmethod
    def requestwithfile(url, values,file_id,file,filename=None):
        if not filename:
            files = {file_id: file}
        else:
            files = {file_id: (filename, file)}
        html = requests.post(url,params=values,files=files)
        logger.debug("Text: " + str(html.text))
        logger.debug("STATUS:"+str(html.status_code))
        return html.json()

    @staticmethod
    def requestwithdata(url,values,data):
        html = requests.post(url,params=values,data=data)
        logger.debug("URL: " + str(html.text))
