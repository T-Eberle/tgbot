# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.config.tgbotfileidparser import TGBotFileIDParser
from telegram.tglogging import logger
from telegram.basicapi.commands.stickercommands import StickerController
from telegram.basicapi.commands.messagecommands import MessageController
from telegram.basicapi.commands.voicecommands import VoiceController
from telegram.basicapi.decorator.tgcommands import *
from socket import *
import random

entertaincommands = ["drunk", "alarm", "macarena", "fu"]

config = TGBotFileIDParser()
data = config.load()


class EntertainCommands:

    def drunk(self,message):
        a = random.randint(1,4)
        StickerController.sendsticker(message.chat_id(), "paul_drunk%s.webp" %a)

    def fu(self, message):
        StickerController.sendsticker(message.chat_id(), "finger.webp")

    def macarena(self,message):
        VoiceController.sendvoice(message.chat_id(), "macarena.mp3")

    def alarm(self,message):
        VoiceController.sendvoice(message.chat_id(), "alarm.mp3")