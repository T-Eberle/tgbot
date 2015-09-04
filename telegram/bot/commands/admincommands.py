# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'
from telegram.tglogging import logger
from telegram.bot.commands import *
from telegram.config.jsonconfigreader import JSONConfigReader
from telegram.basicapi.commands.messagecommands import MessageController
import uwsgi
from telegram.tgredis import setfilevalue,deleteentryfromfile

admincommands = ["restart","reggroup","unreggroup",
                 # "unregisterall",
                 "groupstream"]

class AdminCommands:

    def parseadmincommands(self,message,text):
        logger.debug(text+" command recognized.")
        for registercommand in admincommands:
            if getcommand(text)==registercommand:
                getattr(self, registercommand)(message,text)

    def restart(self,message,text):
        logger.debug("Server will shutdown!")
        MessageController.sendreply(message, message.chat_id(), "Ich, Butler Elroy, werde jetzt neu gestartet.")
        uwsgi.reload()


    def reggroup(self,message,text):
        chat = message.chat
        value = {"title":chat.title}
        logger.debug("VALUE: "+str(value))
        setfilevalue("groups",message.chat_id(),value)
        MessageController.sendreply(message, message.chat_id(), "Der Gruppenchat "+value["title"]+" wurde erfolgreich registriert.")

    def unreggroup(self,message,text):
        user = message.from_User
        deleteentryfromfile("groups",message.chat_id())
        MessageController.sendreply(message, message.chat_id(), user.first_name+", du hast die Gruppe aus den registrierten Gruppen gelöscht.")


    # def unregisterall(self,message,text):
    #     user = message.from_User
    #     jsonusers.deleteall()
    #     MessageController.sendreply(message, message.chat_id(), user.first_name+", du hast alle Users gelöscht. Sei stolz auf dich.")

    def groupstream(self,message,text):
        param = getparameter(text)
        chat = message.chat
        values = getfilevalue("groups",message.chat_id())
        logger.debug("VALUE GROUPSTREAM: "+str(values))
        if param:
            if not values:
                dump = {"title":chat.title,"stream":param}
                setfilevalue("groups",message.chat_id(),dump)
            else:
               values["stream"]=param
               setfilevalue("groups",message.chat_id(),values)

            MessageController.sendreply(message, message.chat_id(), "Stream der Gruppe wurde auf "+param+" gesetzt.")
        else:
            try:
                del values["stream"]
                setfilevalue("groups",message.chat_id(),values)
                MessageController.sendreply(message, message.chat_id(), "Streamparameter für"+values["title"]+ "zurückgesetzt.")
            except KeyError as error:
                logger.warn(str(error) +" - Eintrag in dem Dictionary nicht vorhanden.")
            except TypeError as error:
                logger.warn(str(error) +" - Eintrag in dem Dictionary nicht vorhanden.")