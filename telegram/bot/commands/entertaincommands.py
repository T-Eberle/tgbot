# -*- coding: utf-8 -*-
__author__ = 'Thomas & Carsten'

import random

import pkg_resources

from telegram.bot.commands import *
from telegram.basicapi.commands import sendsticker, sendvoice,sendaudio,sendphotofromurl,sendphoto
from telegram.basicapi.decorator.tgcommands import text
from telegram.bot.decorators import limited
from telegram.basicapi.decorator.permissions import grouptype,permitted
from telegram.config.ninegagapiparser import NineGagApiParser
from telegram.config.tgbotfileidparser import TGBotFileIDParser
from telegram.bot.decorators.onestreamcommand import onestreamcommand
from telegram.config.waoapiparser import WAOAPIParser
from telegram.tgredis import *

huly_list = ["FAULER SACK DU"]

config = TGBotFileIDParser()
data = config.load()


class EntertainCommands:
    def __init__(self):
        self.radiostream = ""

    @permitted
    @grouptype("fun")
    @limited
    def macarena(self,message):
        file = pkg_resources.resource_filename("resources.voice","macarena.mp3")
        sendvoice(message.chat_id(),file)

    @permitted
    @grouptype("fun")
    @limited
    def alarm(self,message):
        file = pkg_resources.resource_filename("resources.voice","alarm.mp3")
        sendaudio(message.chat_id(),file)

    @permitted
    @grouptype("fun")
    @limited
    def haha(self,message):
        file = pkg_resources.resource_filename("resources.voice","haha.mp3")
        sendvoice(message.chat_id(),file)

    @permitted
    @grouptype("fun")
    @limited
    def geil(self,message):
        file = pkg_resources.resource_filename("resources.voice","wardasgeil.mp3")
        sendvoice(message.chat_id(),file)

    @permitted
    @grouptype("fun")
    @limited
    def drunk(self,message):
        file = pkg_resources.resource_filename("resources.img", "drunk%s.webp" % random.randint(1,5))
        sendsticker(message.chat_id(), "Drunk",file)


    @permitted
    @grouptype("fun")
    @limited
    def fu(self, message):
        file = pkg_resources.resource_filename("resources.img", "finger.webp")
        sendsticker(message.chat_id(),"FU",file)

    @permitted
    @grouptype("fun")
    @limited
    def ateam(self,message):
        file = pkg_resources.resource_filename("resources.img", "ateam.webp")
        sendsticker(message.chat_id(),"Ateam", file)

    @permitted
    @grouptype("fun")
    @limited
    def wat(self,message):
        file = pkg_resources.resource_filename("resources.img","wat.gif")
        sendphoto(message.chat_id(),None,open(file,"rb"),"WAT?")

    @permitted
    @grouptype("fun")
    @limited
    @text
    def rallyemaster(self,message):
        return message.chat_id(), "Zitat Rallyemaster1990: \"Wieder mal geile Show mach weiter so\""

    @permitted
    @grouptype("fun")
    @onestreamcommand
    def huly(self,message):
        size_result = len(huly_list)
        rand = random.randint(0, size_result - 1)
        try:
            if WAOAPIParser.now(self.radiostream,"dj"):
                waoapi = WAOAPIParser()
                huly_list.append("%s runterschmeiss" % getdjnamebyonair(waoapi.now(self.radiostream, "dj"),
                                                                        str(waoapi.now(self.radiostream,"djid"))))
                size_result = len(huly_list)
                rand = random.randint(0,size_result - 1)
                return message.chat_id(), str("Zitat Thomas Huly: \"" + huly_list[rand] + "\"")
            else:
                return message.chat_id(),str("Zitat Thomas Huly: \"" + huly_list[rand] + "\"")
        except KeyError as error:
            logger.exception(error)
            return message.chat_id(),str("Zitat Thomas Huly: \"" + huly_list[rand] + "\"")

    @permitted
    @grouptype("fun")
    @limited
    def gag(self,message):
        values = NineGagApiParser.ninegag()
        sendphotofromurl(message.chat_id(),None,values[1],caption=values[0])

    @permitted
    @grouptype("fun")
    @limited
    def pr0(self,message):
        values = NineGagApiParser.pr0gramm()
        sendphotofromurl(message.chat_id(),None,values,caption="Pic from pr0gramm.com")

    @permitted
    @grouptype("fun")
    @limited
    def xkcd(self,message):
        jsondata = NineGagApiParser.xkcd()
        sendphotofromurl(message.chat_id(),None,jsondata["img"],caption=jsondata["safe_title"])

