__author__ = 'Thomas Eberle'

import json
import re
import tempfile
import tgbot
import requests

from tgbot.basicapi.http.httprequestcontroller import HTTPRequestController
from tgbot.config.tgbotconfigparser import TGBotConfigParser
from tgbot.tglogging import logger
from tgbot.basicapi.model.message import Message

suffix = re.compile(r"^(.*/)*(?P<suffix>\w+)$")

basicconfig = TGBotConfigParser("basicconfig.ini","tgbot.resources.config")
basicdata = basicconfig.load()

def sendrequest(method_name,oldvalues={},markdown=True,**kwargs):
    values = oldvalues
    for key in kwargs:
        values[str(key)] = kwargs[key]
    url = basicdata.get("tgapi", "bot_link")+tgbot.iniconfig.get("basics","bot_id")+"/"+basicdata.get("tgapi", method_name + "_Method")
    if markdown:
        values["parse_mode"] = "Markdown"
        jsonfile =  HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values)
        if jsonfile["ok"] and markdown:
            return jsonfile
        else:
            del values["parse_mode"]
            return HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values)
    else:
        return HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values)

def sendrequestwithfile(method_name,file_id,file,filename=None,oldvalues={},
                        **kwargs):
    values = oldvalues
    for key in kwargs:
        values[str(key)] = kwargs[key]
    url = basicdata.get("tgapi", "bot_link")+tgbot.iniconfig.get("basics","bot_id")+"/"+basicdata.get("tgapi", method_name + "_Method")
    # values["parse_mode"] = "Markdown"
    answer =  HTTPRequestController.requestwithfile(url,values,file_id,file,filename)
    checkanswer(answer)

def answerInline(inline_query_id,results,oldValues={}):
    return sendrequest("answerInlineQuery",oldvalues=oldValues,inline_query_id=inline_query_id,results=json.dumps(results))

def sendmessage(oldvalues={},markdown=True,**kwargs):
    answer = sendrequest("sendMessage",oldvalues=oldvalues,markdown=markdown,**kwargs)
    checkanswer(answer)

def sendtextwithoutmarkup(chat_id, text):
    logger.debug("Text sent! -> " + text)
    return sendmessage(chat_id=chat_id,text=text,oldvalues={})

def sendtext(chat_id, text, markdown = True):
    logger.debug("Text sent! -> " + text)
    answer = sendmessage(chat_id=chat_id,text=text,oldvalues={},markdown=markdown)

def sendreply_markup(values,**kwargs):
    markup_values = {}
    for key in kwargs:
        markup_values[str(key)] = kwargs[key]
    return sendmessage(oldvalues=values,reply_markup=json.dumps(markup_values))


def sendreply(message: Message, chat_id, text):
    logger.debug("Reply sent! -> " + text)
    return sendmessage(chat_id=chat_id,text=text,
                                  reply_to_message_id=message.message_id)


def sendforcereply(message: Message, chat_id, text,**kwargs):
    values = {"chat_id": chat_id,"text": text}
    for key, value in kwargs.items():
        values[key] = value
    logger.debug("Forced Reply sent! -> " + text)
    return sendreply_markup(values,force_reply=True,selective=True)


def sendreply_one_keyboardmarkup(message,chat_id,text,keyboard,resize_keyboard=False,**kwargs):
    values = {"chat_id": chat_id, "text": text}
    for key, value in kwargs.items():
        values[key] = value
    return sendreply_markup(values,keyboard=keyboard,
                                       one_time_keyboard=True,selective=True,resize_keyboard=resize_keyboard)


def hide_keyboard(message,chat_id,text,**kwargs):
    values = {"chat_id": chat_id, "text": text}
    for key, value in kwargs.items():
        values[key] = value
    return sendreply_markup(values,hide_keyboard=True,selective=True)


def sendvoice(chat_id, file):
    return sendrequestwithfile("sendVoice","voice",open(file,"rb"),filename=None,chat_id=chat_id)


def sendaudio(chat_id,filename,file):
    return sendrequestwithfile("sendAudio","audio",open(file,"rb"),filename=filename,chat_id=chat_id)


def sendsticker(chat_id, stickername,sticker):
    return sendrequestwithfile("sendSticker","sticker",
                        open(sticker,"rb"),filename=stickername,chat_id=chat_id)


def senddocument(chat_id,filename,file):
    return sendrequestwithfile("sendDocument","document",file,filename=filename,chat_id=chat_id)


def sendstringasfile(chat_id,file_id,filename,filestring):
    return sendrequestwithfile("sendDocument",file_id,filestring,filename=filename,chat_id=chat_id)


def sendphoto(chat_id, photoname,photo,caption=None,**kwargs):
    return sendrequestwithfile("sendPhoto","photo",photo,filename=photoname,chat_id=chat_id,caption=caption,**kwargs)


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
                return senddocument(chat_id,photoname,temp)
            else:
                return sendphoto(chat_id,photoname,temp,caption=caption)
            temp.close()


def sendphoto_hidekeyboard(message,chat_id, photoname,photo,caption=None):
        markup_values = {"hide_keyboard":True,"selective":True}
        return sendphoto(chat_id, photoname,photo,caption=caption,
                  reply_markup=json.dumps(markup_values))


def sendChatAction(chat_id,chataction):
    return sendrequest("sendChatAction",chat_id=chat_id,action=chataction)


# Hilfsmethoden

def checkanswer(answer):
    message = tgbot.mainmessage
    if not message:
        return
    error_msg_403 = tgbot.iniconfig.get("error_messages","403")
    error_msg_peer_invalid = tgbot.iniconfig.get("error_messages","PEER_INVALID")
    user = message.from_User
    error_code = answer.get("error_code")
    if error_code == 403:
        sendtext(message.chat_id(),"%s, %s \n"
                                   "Fehlermeldung: ```%s```"%(user.first_name,error_msg_403,answer.get("description")))
    elif error_code == 400 and "PEER_ID_INVALID" in answer.get("description"):
        sendtext(message.chat_id(),"%s, %s \n"
                                   "Fehlermeldung: ```%s```"%
                 (user.first_name,error_msg_peer_invalid,answer.get("description")))