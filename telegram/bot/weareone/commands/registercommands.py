__author__ = 'Thomas Eberle'

from telegram.bot.tglogging.TGLogger import logger
from telegram.bot.basicapi.commands.messagecommands import MessageController
from telegram.bot.weareone.commands.commandutilities import *
from telegram.bot.tgredis.tgredishandler import *

registercommands = ["register","unregister"]

class RegisterCommands:

    def parseregistercommands(self,message,text):
        logger.debug("/"+text+" command recognized.")
        for registercommand in registercommands:
            if getcommand(text)==registercommand:
                getattr(self, registercommand)(message)



    def register(self, message):
        MessageController.sendreply(message, message.chat_id(), "Witzbold.")

    def unregister(message):
         MessageController.sendreply(message, message.chat_id(), "Witzbold.")
