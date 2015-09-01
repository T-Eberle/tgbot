# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import re
import json
from datetime import  datetime,timedelta

from pytz import timezone

from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger
from telegram.config.jsonconfigreader import JSONConfigReader


regex =re.compile(r'/(?P<command>\w+)(\s(?P<parameter>.+))?')
oldtimeformat = "%A, %d.%m.%y %H:%M"
timeformat = "%H:%M"
daytimeformat ="%a %H:%M"
de_timezone = timezone("Europe/Berlin")
wochentag=["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]


config = TGBotConfigParser("config.ini")
data = config.load()



jsonuser = JSONConfigReader("users")


jsongroup = JSONConfigReader("groups")

def getparameter(text,alternative_text=None):
    m = regex.match(text)
    if not m:
        return ""
    else:
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
    value = m.group("command")
    value.lower()
    return value

def printshowplan(data):
    reply =""
    for show in data:
        start =getcorrectdateinstring(int(show["start "]))
        ende = getcorrectdateinstring(show["end"]-int(show["start "]))
        reply +=createshowstring(show,start,ende)

    return reply

def nextshow(data,stream):
    jsonuser.read()
    jsonfile = jsonuser.jsondata
    for show in data:
        reply= "\U00002139Nächste Show @ " + stream.capitalize() + "\U00002139\n"
        start = getcorrectdate(int(show["start "]))
        startofficial =dateindaytimeformat(int(show["start "]))
        ende = dateindaytimeformat(show["end"]-int(show["start "]))
        now = datetime.now()
        if start > now:
            reply+=createshowstring(show,startofficial,ende,jsonfile)
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

def dateindaytimeformat(showdate):
    return getcorrectdate(showdate).strftime(daytimeformat)

def getshowfromtoday(data,stream):
    return getshowfromday(data,getcorrectdate(datetime.now().timestamp()).weekday(),stream)

def getshowfromtomorrow(data,stream):
    tomorrow = datetime.now()+timedelta(days=1)
    return getshowfromday(data,getcorrectdate(tomorrow.timestamp()).weekday(),stream)


def getshowfromday(data,date,stream):
        now = datetime.now().date()
        result_date = now
        jsonuser.read()
        jsonfile = jsonuser.jsondata
        while result_date.weekday() != date:
            result_date+=timedelta(days=1)
        reply="\U00002139"+"Shows am " + wochentag[date] + " @ " + stream.capitalize()+"\U00002139\n"
        showstring = ""
        for show in data:
            start = getutcdate(int(show["start "]))
            end = getcorrectdate(show["end"]-int(show["start "]))
            if start.date()==result_date<=end.date():
                start_string =getcorrectdateinstring(int(show["start "]))
                end_string = getcorrectdateinstring(show["end"]-int(show["start "]))
                showstring += createshowstring(show,start_string,end_string,jsonfile)
        if not showstring:
            reply+= str('''\U0001F44E\U0001F44E\U0001F44EKEINE SHOW VORHANDEN!''')
            logger.debug("REPLY: "+reply)
            return reply
        else:
            reply +=showstring
            logger.debug("REPLY: "+reply)
            return reply
def getDJNameByShow(show,jsonfile):
    name = None
    for key, value in jsonfile.items():
        if value.get("wao_id") == show["user_id"]:
            name = "@"+value.get("user_name")
            logger.debug("WeAreOne-ID found. Telegram Chat ID: "+ str(key))
    if not name:
        name = show["username"]
    return name

def getDJNameByOnAir(dj,id,jsonfile):
    name = None
    for key, value in jsonfile.items():
        if value.get("wao_id") == id:
            name = "@"+value.get("user_name")
            logger.debug("WeAreOne-ID found. Telegram Chat ID: "+ str(key))
    if not name:
        name = dj
    return name

def createshowstring(show,start,ende,jsonfile):
    name = getDJNameByShow(show,jsonfile)

    showname = show["showname"]
    if not showname:
        return str('''\U0001F3A4Show by %s
\U000023F0Zeit: %s - %s
''' % (name,str(start,str(ende))))

    else:
        return str('''\U0001F3A4Show: \"%s\" by %s
\U000023F0Zeit: %s - %s
''' % (show["showname"],name,str(start),str(ende)))

def getStreamParameter(message):
    user = message.from_User
    jsonuser.read()
    jsongroup.read()
    uservalues = jsonuser.getValues(user.chat_id)
    groupvalues = jsongroup.getValues(message.chat_id())
    if uservalues:
        if uservalues.get("stream"):
            logger.debug("USER VALUE USED")
            return uservalues.get("stream")
        elif groupvalues:
            if groupvalues.get("stream"):
                return groupvalues.get("stream")
            else:
                return ""
    elif groupvalues:
        logger.debug("GROUP VALUE USED")
        return groupvalues.get("stream")
    else:
        return ""