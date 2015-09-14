# -*- coding: utf-8 -*-
__author__ = 'Tommy'

from telegram.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.config.tgbotconfigparser import TGBotConfigParser

data = TGBotConfigParser("config.ini").config


class FileController:
    @staticmethod
    def senddocument(chat_id,file_id):
        values = {"chat_id": chat_id}
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendDocument_Method")
        HTTPRequestController.requestwithdoc(url, values,"document",file_id)
        pass

    @staticmethod
    def sendstringasfile(chat_id,file_id,filename,filestring):
        values = {"chat_id": chat_id}
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendDocument_Method")
        HTTPRequestController.requestwithstringasfile(url,values,file_id,filename,filestring)
        pass

    @staticmethod
    def sendfile(chat_id,file_id,filename,file):
        values = {"chat_id": chat_id}
        url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendDocument_Method")
        HTTPRequestController.requestwithfile(url,values,file_id,filename,file)


