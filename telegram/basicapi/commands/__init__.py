__author__ = 'Thomas Eberle'

from telegram.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.config.tgbotconfigparser import TGBotConfigParser
from requests.exceptions import HTTPError
from telegram.tglogging import logger
from telegram.basicapi.model.message import Message
import json

config = TGBotConfigParser("config.ini")
data = config.load()


def dosomething(method_name,oldvalues,**kwargs):
    values = oldvalues
    for key in kwargs:
        values[str(key)] = kwargs[key]
    url = data.get("tgapi", "bot_link") + data.get("tgapi", method_name + "_Method")
    values["parse_mode"] = "Markdown"
    try:
        HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values)
    except HTTPError:
        del values["parse_mode"]
        HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values)


def dosomethingwithfile(method_name,file_id,filename,oldvalues={},path="resources.documents",complete_path=None,
                        **kwargs):
    values = oldvalues
    for key in kwargs:
        values[str(key)] = kwargs[key]
    url = data.get("tgapi", "bot_link") + data.get("tgapi", method_name + "_Method")
    values["parse_mode"] = "Markdown"
    HTTPRequestController.requestwithdoc(url,values,file_id,filename,path=path,complete_path=complete_path)

def sendmessage(oldvalues={},**kwargs):
    dosomething("sendMessage",oldvalues=oldvalues,**kwargs)


def sendtext(chat_id, text):
    logger.debug("Text sent! -> " + text)
    req = sendmessage(chat_id=chat_id,text=text)
    if req == 400:
        sendmessage(chat_id=chat_id,text=text)


def sendreply_markup(values,**kwargs):
    markup_values = {}
    for key in kwargs:
        markup_values[str(key)] = kwargs[key]
    sendmessage(oldvalues=values,reply_markup=json.dumps(markup_values))


def sendreply(message: Message, chat_id, text):
    logger.debug("Reply sent! -> " + text)
    sendmessage(chat_id=chat_id,text=text,
                                  reply_to_message_id=message.message_id)


def sendforcereply(message: Message, chat_id, text):
    values = {"chat_id": chat_id, "reply_to_message_id": message.message_id,"text": text}
    logger.debug("Forced Reply sent! -> " + text)
    sendreply_markup(values,force_reply=True,selective=True)


def sendreply_one_keyboardmarkup(message,chat_id,text,keyboard,resize_keyboard=False):
    values = {"chat_id": chat_id, "text": text, "reply_to_message_id": message.message_id}
    sendreply_markup(values,keyboard=keyboard,
                                       one_time_keyboard=True,selective=True,resize_keyboard=resize_keyboard)


def hide_keyboard(message,chat_id,text):
    values = {"chat_id": chat_id, "text": text, "reply_to_message_id": message.message_id}
    sendreply_markup(values,hide_keyboard=True,selective=True)


def sendvoice(chat_id, voice,complete_path=None):
    dosomethingwithfile(method_name="sendVoice",file_id="voice",
    filename=voice,path="resources.voice",chat_id=chat_id,complete_path=complete_path)


def sendstickerwithid(chat_id, file_id):
    url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendSticker_Method")
    values = {'chat_id': chat_id}
    HTTPRequestController.requestwithimg(url, values,file_id)
    logger.debug("Sticker sent! -> ID #" + file_id)


def sendsticker(chat_id, sticker,complete_path=None):
    dosomethingwithfile(method_name="sendSticker",file_id="sticker",
                        filename=sticker,path="resources.img",chat_id=chat_id,complete_path=complete_path)

def senddocument(chat_id,file_id):
    values = {"chat_id": chat_id}
    url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendDocument_Method")
    HTTPRequestController.requestwithdoc(url, values,"document",file_id)


def sendstringasfile(chat_id,file_id,filename,filestring):
    values = {"chat_id": chat_id}
    url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendDocument_Method")
    HTTPRequestController.requestwithstringasfile(url,values,file_id,filename,filestring)


def sendfile(chat_id,file_id,filename,file):
    values = {"chat_id": chat_id}
    url = data.get("tgapi", "bot_link") + data.get("tgapi", "sendDocument_Method")
    HTTPRequestController.requestwithfile(url,values,file_id,filename,file)


