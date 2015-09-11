# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import requests
import traceback
import pkg_resources
from telegram.tglogging import *


class HTTPRequestController:
    def __init__(self, url=None, values=None):
        self.url = url
        self.values = values

    @staticmethod
    def requestwithvaluesxwwwurlencoded(url, values):
        req = requests.post(url,params=values)
        # data = urlencode(values)
        # data = data.encode("utf-8")
        #
        # request = Request(url)
        # request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
        logger.debug("URL: "+str(req.url))
        # response = urlopen(request.get_full_url(), data)
        # html = response.read()
        return req.raise_for_status()


    @staticmethod
    def requestwithimg(url, values,filename):
        logger.debug("URL: " + str(url))
        file = pkg_resources.resource_filename("resources.img", filename)
        logger.debug("FILE: "+str(file))
        files = {"sticker": open(file,"rb")}
        html = requests.post(url,data=values,files=files)

    @staticmethod
    def requestwithdoc(url, values,file_id,filename,path="resources.documents",complete_path=None):
        logger.debug("URL: " + str(url))
        if not complete_path:
            file = pkg_resources.resource_filename(path, filename)
        else:
            file = complete_path
        logger.debug("PATH: "+str(path))
        logger.debug("FILE: "+str(filename))
        files = {file_id: (filename,open(file,"rb"))}
        html = requests.post(url,data=values,files=files)

    @staticmethod
    def requestwithstringasfile(url, values,file_id,filename,filestring):
        logger.debug("URL: " + str(url))
        logger.debug("FILE: "+str(filename))
        files = {file_id: (filename,filestring)}
        html = requests.post(url,data=values,files=files)
