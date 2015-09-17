# -*- coding: utf-8 -*-
__author__ = 'Thomas & Carsten'

import random
from telegram.bot.commands import *
from telegram.basicapi.commands.stickercommands import StickerController
from telegram.basicapi.commands.voicecommands import VoiceController
from telegram.basicapi.decorator.tgcommands import *
from telegram.bot.decorators import limited
from telegram.config.ninegagapiparser import NineGagApiParser
from telegram.config.tgbotfileidparser import TGBotFileIDParser
from telegram.bot.decorators.onestreamcommand import onestreamcommand
from telegram.config.waoapiparser import WAOAPIParser

from telegram.tgredis import *

entertaincommands = ["drunk", "alarm", "macarena", "fu", "gag", "pr0", "ateam", "rallyemaster", "huly"]
huly_list = ["FAULER SACK DU"]

config = TGBotFileIDParser()
data = config.load()


class EntertainCommands:
    def __init__(self):
        self.radiostream = ""

    @limited
    def macarena(self,message):
        VoiceController.sendvoice(message.chat_id(), "macarena.mp3")

    @limited
    def alarm(self,message):
        VoiceController.sendvoice(message.chat_id(), "alarm.mp3")

    @limited
    def haha(self,message):
        VoiceController.sendvoice(message.chat_id(), "haha.mp3")

    @limited
    def geil(self,message):
        VoiceController.sendvoice(message.chat_id(), "wardasgeil.mp3")

    @limited
    def drunk(self,message):
        StickerController.sendsticker(message.chat_id(), "drunk%s.webp" % random.randint(1,5))

    @limited
    def fu(self, message):
        StickerController.sendsticker(message.chat_id(), "finger.webp")

    @limited
    def ateam(self,message):
        StickerController.sendsticker(message.chat_id(), "ateam.webp")

    @limited
    def rallyemaster(self,message):
        MessageController.sendtext(message.chat_id(), "Zitat Rallyemaster1990: \"Wieder mal geile Show mach weiter so\""
                                                      "")

    @onestreamcommand
    def huly(self,message):
        if WAOAPIParser.now("HouseTime","dj"):
            waoapi = WAOAPIParser()
            huly_list.append("%s runterschmeiss" % getdjnamebyonair(waoapi.now("Housetime", "dj"),
                                                                    str(waoapi.now("Housetime","djid"))))
            size_result = len(huly_list)
            rand = random.randint(0,size_result - 1)
            return message.chat_id(), str("Zitat Thomas Huly: \"" + huly_list[rand] + "\"")
        else:
            size_result = len(huly_list)
            rand = random.randint(0, size_result - 1)
            return message.chat_id(),str("Zitat Thomas Huly: \"" + huly_list[rand] + "\"")
#        return ausgabe

    @limited
    @sendtext
    def gag(self,message):
        return message.chat_id(),NineGagApiParser.ninegag()

    @limited
    @sendtext
    def pr0(self,message):
        return message.chat_id(),NineGagApiParser.pr0gramm()
