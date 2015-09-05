# -*- coding: utf-8 -*-
__author__ = 'Tommy'

from telegram.basicapi.commands.messagecommands import MessageController
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.config.weareonejsonparser import WeAreOneJSONParser
from datetime import datetime
from telegram.bot.commands.radiocommands import radiostreams
from telegram.tglogging import *
from telegram.tgredis import getfile, getfilevalue

timeformat = "%A, %H:%M"
config = TGBotConfigParser("config.ini")
data = config.load()
controller = MessageController()
waoParser = WeAreOneJSONParser("housetime_onAir")
primetime_start = int(data["primetime"]["primetime_start"])
primetime_end = int(data["primetime"]["primetime_end"])


def checkprimetime():
    """
    Prüft ob in der Primetime eines Streams Lücken vorhanden sind.
    Dies ist Gruppenabhängig, da in der Gruppe der Gruppenstream festgelegt wird.
    Dieser Gruppenstream wird dann immer zu einer bestimmten Uhrzeit auf Lücke überprüft.
    """
    now = datetime.now()
    keys = getfile("groups").keys()
    for key in keys:
        result = ""
        value = getfilevalue("groups", key)
        for radiostream in radiostreams.items():
            if radiostream[0] in value.get("stream") or radiostream[1] in value.get("stream"):
                showplan = waoParser.load(radiostream[1] + "_shows")

                today = now.date()
                times = []
                for show in showplan:
                    start = datetime.fromtimestamp(int(show["start "]))
                    end = datetime.fromtimestamp(int(show["end"] - int(show["start "])))
                    if today == start.date():
                        end_hour = end.hour
                        if end.hour == 0:
                            end_hour = 24
                        for showtime in range(start.hour, end_hour):
                            times.append(showtime)

                logger.debug("Primetimestart: " + str(primetime_start) + ", Primetimeend: " + str(
                    primetime_end) + ", Times: " + str(times))
                djwanted = ""
                for showtime in range(primetime_start, primetime_end):

                    if not (showtime in times) and now.hour <= showtime:
                        djwanted += "\U000027A1" + str(showtime) + ":00 - " + str(showtime + 1) + ":00 \n"
                if djwanted:
                    result += "\U000026A0DJ WANTED @ " + radiostream[
                        1].capitalize() + " für folgende Zeiten\U000026A0\n" + djwanted
        if result:
            controller.sendmessage(key, result)
        else:
            logger.debug("checkPrimetime: No times in Primetime available.")
