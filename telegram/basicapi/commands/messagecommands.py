# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'


from telegram.basicapi.model.message import Message
from telegram.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger
from telegram.basicapi.commands import dosomething
import requests
from requests.exceptions import HTTPError
import json





class MessageController:
    def __init__(self, message: Message=None):
        self.message = message


    @staticmethod
    def sendmessage(oldvalues = {},**kwargs):
        dosomething("sendMessage",oldvalues=oldvalues,**kwargs)


    @staticmethod
    def sendtext(chat_id, text):
        logger.debug("Text sent! -> " + text)
        req = MessageController.sendmessage(chat_id=chat_id,text=text)
        if req==400:
            MessageController.sendmessage(chat_id=chat_id,text=text)


    @staticmethod
    def sendreply_markup(values,**kwargs):
        markup_values={}
        for key in kwargs:
            markup_values[str(key)]=kwargs[key]
        MessageController.sendmessage(oldvalues=values,reply_markup=json.dumps(markup_values))

    @staticmethod
    def sendreply(message: Message, chat_id, text):
        logger.debug("Reply sent! -> " + text)
        MessageController.sendmessage(chat_id=chat_id,text=text,
                                      reply_to_message_id=message.message_id)

    @staticmethod
    def sendforcereply(message: Message, chat_id, text):
        values = {"chat_id": chat_id, "reply_to_message_id": message.message_id,"text": text}
        logger.debug("Forced Reply sent! -> " + text)
        MessageController.sendreply_markup(values,force_reply=True,selective=True)

    @staticmethod
    def sendreply_one_keyboardmarkup(message,chat_id,text,keyboard,resize_keyboard=False):
        values = {"chat_id": chat_id, "text": text, "reply_to_message_id": message.message_id}
        MessageController.sendreply_markup(values,keyboard=keyboard,
                                           one_time_keyboard=True,selective=True,resize_keyboard=resize_keyboard)

    @staticmethod
    def hide_Keyboard(message,chat_id,text):
        values = {"chat_id": chat_id, "text": text, "reply_to_message_id": message.message_id}
        MessageController.sendreply_markup(values,hide_keyboard=True,selective=True)

