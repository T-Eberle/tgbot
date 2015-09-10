# -*- coding: utf-8 -*-
__author__ = 'Tommy'

from telegram.basicapi.commands.messagecommands import MessageController
from telegram.basicapi.commands.filecommands import FileController
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.config.waoapiparser import WAOAPIParser
from datetime import datetime,timedelta
import collections
from telegram.tglogging import *
from telegram.tgredis import getfile, getfilevalue

timeformat = "%A, %H:%M"
config = TGBotConfigParser("config.ini")
data = config.load()
controller = MessageController()
waoParser = WAOAPIParser("housetime_onAir")
primetime_start = int(data["primetime"]["primetime_start"])
primetime_end = int(data["primetime"]["primetime_end"])

waoconfig = TGBotConfigParser("wao-config.ini")
waodata =waoconfig.load()

unsorted_radiostreams = {"tb": "technobase", "ht": "housetime", "hb": "hardbase", "trb": "trancebase", "ct": "coretime",
                         "clt": "clubtime"}
radiostreams = collections.OrderedDict(sorted(unsorted_radiostreams.items()))

def getTracklist():
    now = datetime.now()
    keys = getfile("groups").keys()
    for key in keys:
        try:


            value = getfilevalue("groups", key)
            for radiostream in radiostreams.items():
                complete_result = ""
                streamfile=""
                stream = value.get("stream")
                if radiostream[0] in stream or radiostream[1] in stream:

                    waoapi = WAOAPIParser(stream=radiostream[1])
                    tracks = waoapi.loadwaoapitracklist(count=20, upcoming=True)

                    stream_title = "\n\nTracklist für %s: \n" % radiostream[1].capitalize()
                    result = ""
                    for track in tracks:
                        start_timestamp = track[waodata.get("waoapi-tracklist", "playtime")]
                        start_date_string = WAOAPIParser.correctdate_timeformat(int(start_timestamp), format="%a %H:%M")
                        start_date = WAOAPIParser.correcdate(start_timestamp)
                        now = datetime.now()
                        delta = timedelta(minutes=now.minute)
                        now_rounded = now - delta
                        if now_rounded - start_date <= timedelta(hours=1) and start_date < now_rounded:
                            artist = track[waodata.get("waoapi-tracklist", "artist")]
                            title = track[waodata.get("waoapi-tracklist", "title")]
                            moderator = track[waodata.get("waoapi-tracklist","moderator")]

                            result += start_date_string + ": " + artist + " - " + title + "\n"
                    if result:
                        complete_result += stream_title + result + "\n"
                        streamfile+="_"+radiostream[0]+"_"+moderator
                    if complete_result:
                        FileController.sendStringasFile(int(key),"document","tracklist"+streamfile+".txt",complete_result)
                    else:
                        logger.warn("No Tracklist @ "+radiostream[1]+" available.")
                        continue
        except TypeError:
            logger.warn("No stream set.")


def checkprimetime():
    """
    Prüft ob in der Primetime eines Streams Lücken vorhanden sind.
    Dies ist Gruppenabhängig, da in der Gruppe der Gruppenstream festgelegt wird.
    Dieser Gruppenstream wird dann immer zu einer bestimmten Uhrzeit auf Lücke überprüft.
    """
    now = datetime.now()
    keys = getfile("groups").keys()
    for key in keys:
        try:
            result = ""
            value = getfilevalue("groups", key)
            for radiostream in radiostreams.items():
                if radiostream[0] in value.get("stream") or radiostream[1] in value.get("stream"):
                    showplan = waoParser.loadtray(radiostream[1] + "_shows")

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
                controller.sendtext(key, result)
            else:
                logger.debug("checkPrimetime: No times in Primetime available.")
        except TypeError:
            logger.warn("No stream set.")