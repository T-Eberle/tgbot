__author__ = 'Thomas Eberle'

from telegram.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.config.tgbotconfigparser import TGBotConfigParser
from requests.exceptions import HTTPError
from telegram.tglogging import logger
from telegram.basicapi.model.message import Message
import json
import re
import requests
import tempfile

suffix = re.compile(r"^(.*/)*(?P<suffix>\w+)$")

config = TGBotConfigParser("config.ini")
data = config.load()


def sendrequest(method_name,oldvalues={},**kwargs):
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


def sendrequestwithfile(method_name,file_id,file,filename=None,oldvalues={},
                        **kwargs):
    values = oldvalues
    for key in kwargs:
        values[str(key)] = kwargs[key]
    url = data.get("tgapi", "bot_link") + data.get("tgapi", method_name + "_Method")
    values["parse_mode"] = "Markdown"
    HTTPRequestController.requestwithfile(url,values,file_id,file,filename)


def sendmessage(oldvalues={},**kwargs):
    sendrequest("sendMessage",oldvalues=oldvalues,**kwargs)


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


def sendvoice(chat_id, file):
    sendrequestwithfile("sendVoice","voice",open(file,"rb"),filename=None,chat_id=chat_id)


def sendaudio(chat_id,filename,file):
    sendrequestwithfile("sendAudio","audio",open(file,"rb"),filename=filename,chat_id=chat_id)


def sendsticker(chat_id, stickername,sticker):
    sendrequestwithfile("sendSticker","sticker",
                        open(sticker,"rb"),filename=stickername,chat_id=chat_id)


def senddocument(chat_id,filename,file):
    sendrequestwithfile("sendDocument","document",file,filename=filename,chat_id=chat_id)


def sendstringasfile(chat_id,file_id,filename,filestring):
    sendrequestwithfile("sendDocument",file_id,filestring,filename=filename,chat_id=chat_id)


def sendphoto(chat_id, photoname,photo,caption=None):
    sendrequestwithfile("sendPhoto","photo",photo,filename=photoname,chat_id=chat_id,caption=caption)


def sendphotofromurl(chat_id,photoname,url,caption=None):
    sendChatAction(chat_id,"upload_photo")
    logger.debug("PIC URL: %s" % url)
    response = requests.get(url,stream=True)
    content_type = suffix.search(response.headers.get("content-type")).group("suffix")
    logger.debug("CONTENT TYPE: %s" % content_type)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(suffix="."+content_type) as temp:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    temp.write(chunk)
            temp.seek(0)
            if content_type=="gif":
                senddocument(chat_id,photoname,temp)
            else:
                sendphoto(chat_id,photoname,temp,caption=caption)
            temp.close()


def sendChatAction(chat_id,chataction):
    sendrequest("sendChatAction",chat_id=chat_id,action=chataction)
    pass

