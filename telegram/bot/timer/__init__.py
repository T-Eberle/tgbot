# -*- coding: utf-8 -*-
__author__ = 'Tommy'


from telegram.basicapi.commands.messagecommands import MessageController
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.config.weareonejsonparser import WeAreOneJSONParser
from datetime import  datetime
from telegram.bot.commands.radiocommands import radiostreams
from telegram.tglogging import *
from telegram.tgredis import getfile,getfilevalue



timeformat = "%A, %H:%M"
config = TGBotConfigParser("config.ini")
data = config.load()
controller = MessageController()
waoParser = WeAreOneJSONParser("housetime_onAir")
primetime_start = int(data["primetime"]["primetime_start"])
primetime_end= int(data["primetime"]["primetime_end"])

def checkPrimetime():
    now = datetime.now()
    keys = getfile("groups").keys()
    for key in keys:
        result=""
        value = getfilevalue("groups",key)
        for radiostream in radiostreams.items():
            if radiostream[0] in value.get("stream") or radiostream[1] in value.get("stream"):
                showplan = waoParser.load(radiostream[1]+"_shows")

                today = now.date()
                times=[]
                for show in showplan:
                        start = datetime.fromtimestamp(int(show["start "]))
                        end = datetime.fromtimestamp(int(show["end"]-int(show["start "])))
                        if today == start.date():
                            end_hour = end.hour
                            if end.hour == 0:
                                end_hour = 24
                            for time in range(start.hour,end_hour):
                                times.append(time)

                logger.debug("Primetimestart: "+str(primetime_start)+", Primetimeend: "+str(primetime_end)+", Times: "+str(times))
                djwanted=""
                for time in range(primetime_start,primetime_end):

                    if not (time in times) and now.hour<=time:
                        djwanted+= "\U000027A1"+str(time)+":00 - "+str(time+1)+":00 \n"
                if djwanted:
                    result+= "\U000026A0DJ WANTED @ "+radiostream[1].capitalize()+" für folgende Zeiten\U000026A0\n"+djwanted
        if result:
            controller.sendmessage(key,result)
        else:
            logger.debug("checkPrimetime: No times in Primetime available.")
