# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.config.tgbotfileidparser import TGBotFileIDParser
from telegram.tglogging import logger
from telegram.basicapi.commands.stickercommands import StickerController
from telegram.basicapi.commands.messagecommands import MessageController
from telegram.basicapi.commands.voicecommands import VoiceController
from telegram.basicapi.decorator.tgcommands import *

entertaincommands = ["genius", "me gusta", "halt stop", "halt, stop", "halt,stop"]

config = TGBotFileIDParser()
data = config.load()


class EntertainCommands:

    def genius(self,message):
        StickerController.sendstickerwithid(message.chat_id(), data.get("file_ids", "genius"))


    def megusta(self,message):
        StickerController.sendstickerwithid(message.chat_id(), data.get("file_ids", "megusta"))


    def haltstop(self,message):
        MessageController.sendreply(message, message.chat_id(), "JETZT REDE ICH!\n" +
                                    "https://www.youtube.com/watch?v=C1fCJvgNDow")

    def macarena(self,message):
        VoiceController.sendvoice(message.chat_id(), "macarena.ogg")