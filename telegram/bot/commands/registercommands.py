# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.tglogging import logger
from telegram.basicapi.commands.messagecommands import MessageController
from telegram.config.jsonconfigreader import JSONConfigReader
from telegram.bot.commands import *
from telegram.tgredis import getfile,deleteentryfromfile,setfilevalue

allRegcommands = ["register","unregister","stream"]

# Klasse für Registrierbefehle
class RegisterCommands:

    def parseregistercommands(self,message,text):
        logger.debug(text+" command recognized.")
        for registercommand in allRegcommands:
            if getcommand(text).lower()==registercommand:
                getattr(self, registercommand)(message,text.lower())


    # Befehl zum Registrieren des Nutzers
    def register(self, message,text):
        users = getfile("users")
        user = message.from_User
        param = getparameter(text,None)
        values = getfilevalue("users",user.chat_id)
        if not values:
            values = {"first_name":user.first_name,"user_name":user.username,"last_name":user.last_name,"wao_id":param}
        else:
            values["first_name"]= user.first_name
            values["user_name"]= user.username
            values["last_name"]= user.last_name
        if param:
            for key, value in users.items():
                if value.get("wao_id") == param:
                    MessageController.sendmessage(message, message.chat_id(), "\U0000274E"+"Die WAO-ID wurde schon auf folgenden User registriert: @"+value.get("user_name"))
                    return
            values["wao_id"]=param
            setfilevalue("users",user.chat_id,values)

            MessageController.sendmessage(message, message.chat_id(), "\U00002705"+"@"+user.username+ " mit folgendem WeAreOne Account registriert:\n"+
                                        "http://www.technobase.fm/member/"+param)

    # Befehl zum Löschen eines Nutzers aus der Datenbank
    def unregister(self,message,text):
        user = message.from_User
        deleteentryfromfile("users",user.chat_id)
        MessageController.sendreply(message, message.chat_id(), "\U00002705"+user.first_name+", du hast dich erfolgreich ausgetragen. Und tschüss.")




    # Befehl zum Setzen eines oder mehrerer Streams für den jeweiligen Nutzer.
    def stream(self,message,text):
        param = getparameter(text,None)
        user = message.from_User
        values = getfilevalue("users",user.chat_id)
        if param:
            if not values:
                MessageController.sendreply(message, message.chat_id(), "\U0000274E"+user.first_name+", registriere dich erst mit /register, bevor du deinen Stream setzt.")
                return
            values["stream"] = param
            MessageController.sendreply(message, message.chat_id(), "\U00002705"+user.first_name+", du hast deinen Streamparameter auf "+param+" gesetzt.")
        else:
            try:
                del values["stream"]
                MessageController.sendreply(message, message.chat_id(), "\U00002705"+user.first_name+", du hast deinen Streamparameter zurückgesetzt.")
            except KeyError as error:
                logger.warn(str(error) +" - Eintrag in dem Dictionary nicht vorhanden.")
        setfilevalue("users",user.chat_id,values)