# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.config.tgbotfileidparser import TGBotFileIDParser
from telegram.basicapi.commands.stickercommands import StickerController
from telegram.basicapi.commands.voicecommands import VoiceController
from telegram.basicapi.decorator.tgcommands import *
from telegram.config.ninegagapiparser import NineGagApiParser
import random

entertaincommands = ["drunk", "alarm", "macarena", "fu", "gag"]

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

    @sendtext
    def gag(self,message):
        return message.chat_id(),NineGagApiParser.method()