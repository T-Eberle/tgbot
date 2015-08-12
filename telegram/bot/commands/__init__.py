# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import re
import json
from datetime import  datetime

from pytz import timezone

from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger

regex =re.compile(r'/(?P<command>\w+)(\s(?P<parameter>.+))?')
oldtimeformat = "%A, %d.%m.%y %H:%M"
timeformat = "%A, %H:%M"
de_timezone = timezone("Europe/Berlin")
wochentag=["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]


config = TGBotConfigParser("config.ini")
data = config.load()

def getparameter(text,alternative_text=None):
    m = regex.match(text)
    result = m.group("parameter")
    if not result:
        if not alternative_text:
            return ""
        else:
            return alternative_text
    else:
        return result

def getcommand(text):
    m = regex.match(text)
    return m.group("command")

def printshowplan(data):
    reply =""
    for show in data:
        start =getcorrectdateinstring(int(show["start "]))
        ende = getcorrectdateinstring(show["end"]-int(show["start "]))
        reply +=createshowstring(show,start,ende)

    return reply

def nextshow(data,stream):
    for show in data:
        reply= "\U00002139Nächste Show @ " + stream.capitalize() + "\U00002139\n"
        start = getcorrectdate(int(show["start "]))
        startofficial =getcorrectdateinstring(int(show["start "]))
        ende = getcorrectdateinstring(show["end"]-int(show["start "]))
        now = datetime.now()
        if start > now:
            reply+=createshowstring(show,startofficial,ende)
            return reply

def getutcdate(showdate):
    date = datetime.utcfromtimestamp(showdate)
    return date

def getcorrectdate(showdate):
    date = datetime.fromtimestamp(showdate)
    #offset = de_timezone.utcoffset(date)
    #return date+offset
    return date
def getcorrectdateinstring(showdate):
    return getcorrectdate(showdate).strftime(timeformat)

def getshowfromtoday(data,stream):
    return getshowfromday(data,getcorrectdate(datetime.now().timestamp()).weekday(),stream)


def getshowfromday(data,date,stream):
        reply="\U00002139"+"Shows am "+wochentag[date]+" @ " + stream.capitalize()+"\U00002139\n"
        showstring=""
        for show in data:
            start = getutcdate(int(show["start "]))
            startofficial =getcorrectdateinstring(int(show["start "]))
            ende = getcorrectdateinstring(show["end"]-int(show["start "]))
            if start.weekday() == date:
                showstring += createshowstring(show,startofficial,ende)
        if not showstring:
            reply+= str("\U0001F44E\U0001F44E\U0001F44EKEINE SHOW VORHANDEN!")
            logger.debug("REPLY: "+reply)
            return reply
        else:
            reply +=showstring
            logger.debug("REPLY: "+reply)
            return reply


def createshowstring(show,start,ende):
    name = None
    with open(data["json_files"]["json_path"]+"users.json") as f:
        jsonfile = json.load(f)
        for key, value in jsonfile.items():
            if value.get("wao_id") == show["user_id"]:
                name = "@"+value.get("user_name")
                logger.debug("WeAreOne-ID found. Telegram Chat ID: "+ str(key))
    if not name:
        name = show["username"]
    showname = show["showname"]
    if not showname:
        return str("\U0001F3A4Show by " + name
        +"\n"+
                "\U000023F0Zeit: "+str(start)+" - "
                +str(ende)+"\n")

    else:
        return str("\U0001F3A4Show: \""+show["showname"]+"\" by "+name
        +"\n"+
                "\U000023F0Zeit: "+str(start)+" - "
                +str(ende)+"\n")

