__author__ = 'Thomas'

import re
from pytz import timezone
from datetime import  datetime
from telegram.bot.tglogging.TGLogger import logger

regex =re.compile(r'/(?P<command>\w+)(\s(?P<parameter>.+))?')
oldtimeformat = "%A, %d.%m.%y %H:%M"
timeformat = "%A, %H:%M"
de_timezone= timezone("Europe/Berlin")
wochentag=["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]


def getparameter(text,alternative_text):
    m = regex.match(text)
    result = m.group("parameter")
    if not result:
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
        reply= "\U00002139Naechste Show @ " + stream.capitalize() + "\U00002139\n"
        start = getutcdate(int(show["start "]))
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
    offset = de_timezone.utcoffset(date)
    return date+offset

def getcorrectdateinstring(showdate):
    return getcorrectdate(showdate).strftime(timeformat)

def getshowfromtoday(data,stream):
    return getshowfromday(data,getcorrectdate(datetime.now().timestamp()).weekday(),stream)


def getshowfromday(data,date,stream):
        reply="\U00002139"+"Shows am "+wochentag[date]+" @ " + stream.capitalize()+"\U00002139\n"
        for show in data:
            start = getutcdate(int(show["start "]))
            startofficial =getcorrectdateinstring(int(show["start "]))
            ende = getcorrectdateinstring(show["end"]-int(show["start "]))
            if start.weekday() == date:
                reply += createshowstring(show,startofficial,ende)
        return reply


def createshowstring(show,start,ende):
        return str("\U0001F3A4Show: \""+show["showname"]+"\" by "+show["username"]
            +"\n"+
                    "\U000023F0Zeit: "+str(start)+" - "
                    +str(ende)+"\n")


