# -*- coding: utf-8 -*-
__author__ = 'Thomas & Carsten'

from telegram.bot.commands import *
from telegram.basicapi.commands.stickercommands import StickerController
from telegram.basicapi.commands.voicecommands import VoiceController
from telegram.basicapi.decorator.tgcommands import *
from telegram.bot.decorators import limited
from telegram.config.ninegagapiparser import NineGagApiParser
from telegram.bot.decorators.singleradiocommand import singleradiocommand
import random
from telegram.config.tgbotfileidparser import TGBotFileIDParser

entertaincommands = ["drunk", "alarm", "macarena", "fu", "gag", "pr0", "ateam", "rallyemaster", "huly"]
huly_list = ["FAULER SACK DU", "Test123"]

config = TGBotFileIDParser()
data = config.load()


class EntertainCommands:
    def __init__(self):
        self.radiostream = ""

    @limited
    def drunk(self,message):
        StickerController.sendsticker(message.chat_id(), "drunk%s.webp" % random.randint(1,5))

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
    def rallyemaster(self,message):
        MessageController.sendtext(message.chat_id(), "Zitat Rallyemaster1990: \"Wieder mal geile Show mach weiter so\""
                                                      "")

    # @singleradiocommand
    # def huly(self,message):
    #     message.chat_id(), "test"
         # if WAOAPIParser.now(self.radiostream,"playlist"):
         #     size_result = len(huly_list)
         #     rand = random.randint(0, 1)
         #     logger.debug("::::::::::::::::::::::::VORAUSGABEPLAYLIST")
         #     message.chat_id(),str("Zitat Thomas Huly: \"" + huly_list[rand] + "\"")
         # else:
         #     dj = WAOAPIParser.now(self.radiostream,"dj")
         #     djid = str(WAOAPIParser.now(self.radiostream,"djid"))
         #     huly_list.append("%s runterschmeiss" % getdjnamebyonair(dj, djid))
         #     size_result = len(huly_list)
         #     rand = random.randint(0,size_result - 1)
         #     logger.debug("VORAUSGABEKEINEPLAYLIST")
         #     message.chat_id(), str("Zitat Thomas Huly: \"" + huly_list[1] + "\"")
         # logger.debug("ENDEDERFUNKTION")
         # message.chat_id(), str("test")

    @limited
    @sendtext
    def gag(self,message):
        return message.chat_id(),NineGagApiParser.ninegag()

    @limited
    @sendtext
    def pr0(self,message):
        return message.chat_id(),NineGagApiParser.pr0gramm()
