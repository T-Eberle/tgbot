# -*- coding: utf-8 -*-
__author__ = 'Thomas & Carsten'

from telegram.config.tgbotfileidparser import TGBotFileIDParser
from telegram.basicapi.commands.stickercommands import StickerController
from telegram.basicapi.commands.voicecommands import VoiceController
from telegram.basicapi.decorator.tgcommands import *
from telegram.bot.decorators import limited
from telegram.config.ninegagapiparser import NineGagApiParser
import random

entertaincommands = ["drunk", "alarm", "macarena", "fu", "gag", "pr0", "ateam"]

config = TGBotFileIDParser()
data = config.load()


class EntertainCommands:
    @limited
    def drunk(self,message):
        a = random.randint(1,5)
        StickerController.sendsticker(message.chat_id(), "drunk%s.webp" % a)

    @limited
    def fu(self, message):
        StickerController.sendsticker(message.chat_id(), "finger.webp")

    @limited
    def macarena(self,message):
        VoiceController.sendvoice(message.chat_id(), "macarena.mp3")

    @limited
    def alarm(self,message):
        VoiceController.sendvoice(message.chat_id(), "alarm.mp3")

    @limited
    def ateam(self,message):
        StickerController.sendsticker(message.chat_id(), "ateam.webp")

    @limited
    @sendtext
    def gag(self,message):
        return message.chat_id(),NineGagApiParser.ninegag()

    @limited
    @sendtext
    def pr0(self,message):
        return message.chat_id(),NineGagApiParser.pr0gramm()
