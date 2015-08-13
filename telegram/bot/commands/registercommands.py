# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.tglogging import logger
from telegram.basicapi.commands.messagecommands import MessageController
from telegram.config.jsonconfigreader import JSONConfigReader
from telegram.bot.commands import *

allRegcommands = ["register","unregister","stream"]


jsonconfig = JSONConfigReader("users")

class RegisterCommands:

    def parseregistercommands(self,message,text):
        logger.debug(text+" command recognized.")
        for registercommand in allRegcommands:
            if getcommand(text).lower()==registercommand:
                getattr(self, registercommand)(message,text.lower())



    def register(self, message,text):
        jsonconfig.read()
        user = message.from_User
        param = getparameter(text,None)
        values = jsonconfig.getValues(user.chat_id)
        if not values:
            values = {"first_name":user.first_name,"user_name":user.username,"last_name":user.last_name,"wao_id":param}
        else:
            values["first_name"]= user.first_name
            values["user_name"]= user.username
            values["last_name"]= user.last_name
        if param:
            for key, value in jsonconfig.jsondata.items():
                if value.get("wao_id") == param:
                    MessageController.sendmessage(message, message.chat_id(), "\U0000274E"+"Die WAO-ID wurde schon auf folgenden User registriert: @"+value.get("user_name"))
                    return
            values["wao_id"]=param
            jsonconfig.write(user.chat_id,values)

            MessageController.sendmessage(message, message.chat_id(), "\U00002705"+"@"+user.username+ " mit folgendem WeAreOne Account registriert:\n"+
                                        "http://www.technobase.fm/member/"+param)
    def unregister(self,message,text):
        user = message.from_User
        jsonconfig.delete(user.chat_id)
        MessageController.sendreply(message, message.chat_id(), "\U00002705"+user.first_name+", du hast dich erfolgreich ausgetragen. Und tschüss.")





    def stream(self,message,text):
        jsonconfig.read()
        param = getparameter(text,None)
        user = message.from_User
        values = jsonconfig.getValues(user.chat_id)
        if param:
            if not values:
                jsondump = {"first_name":user.first_name,"user_name":user.username,"last_name":user.last_name}
                jsonconfig.write(user.chat_id,jsondump)
                values = jsonconfig.getValues(user.chat_id)
            values["stream"] = param
            jsonconfig.write(user.chat_id,values)
            MessageController.sendreply(message, message.chat_id(), "\U00002705"+user.first_name+", du hast deinen Streamparameter auf "+param+" gesetzt.")
        else:
            try:
                del values["stream"]
                jsonconfig.write(user.chat_id,values)
                MessageController.sendreply(message, message.chat_id(), "\U00002705"+user.first_name+", du hast deinen Streamparameter zurückgesetzt.")
            except KeyError as error:
                logger.warn(str(error) +" - Eintrag in dem Dictionary nicht vorhanden.")