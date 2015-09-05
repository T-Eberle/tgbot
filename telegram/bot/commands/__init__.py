# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import re
from datetime import datetime, timedelta
from telegram.config.tgbotconfigparser import TGBotConfigParser
from telegram.tglogging import logger
from telegram.tgredis import getfile, getfilevalue
from resources import emoji

regex = re.compile(r'/(?P<command>\w+)(\s(?P<parameter>.+))?')
oldtimeformat = "%A, %d.%m.%y %H:%M"
timeformat = "%H:%M"
daytimeformat = "%a %H:%M"
wochentag = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

config = TGBotConfigParser("config.ini")
data = config.load()


def getparameter(text, alternative_text=None):
    """
    Holt sich den Parameter aus dem angegebenen Text heraus
    :param text: Der angegebene Text
    :param alternative_text: Alternativparameter der zurückgegeben wird
    :return: Der Parameterwert
    """
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
    """
    Holt sich den Befehl aus dem angegebenen Text heraus
    :param text: Der angegebene Text
    :return: Der Commandwert
    """
    m = regex.match(text)
    value = m.group("command")
    value.lower()
    return value


def printshowplan(showdata):
    """
    Gibt den kompletten Sendeplan zurück
    :param showdata: Sendeplandatei
    :return: Sendeplan als String
    """
    reply = ""
    for show in showdata:
        start = getdateinstring(int(show["start "]))
        ende = getdateinstring(show["end"] - int(show["start "]))
        reply += createshowstring(show, start, ende)

    return reply


def nextshow(showdata, stream):
    """
    Erstellt einen String der nächsten Show
    :param showdata: Sendeplandatei
    :param stream: der Stream
    :return: String der nächsten Show
    """
    for show in showdata:
        reply = "\U00002139Nächste Show @ " + stream.capitalize() + "\U00002139\n"
        start = getdate(int(show["start "]))
        startofficial = dateindaytimeformat(int(show["start "]))
        ende = dateindaytimeformat(show["end"] - int(show["start "]))
        now = datetime.now()
        if start > now:
            reply += createshowstring(show, startofficial, ende)
            return reply


def getdate(showdate):
    """
    Gibt das Datum von einem Timestamp zurück.
    :param showdate:
    :return: Datum von einem Timestamp
    """
    date = datetime.fromtimestamp(showdate)
    return date


def getdateinstring(showdate):
    """
    Gibt einen String im timeformat von einem Datum zurück.
    :param showdate:
    :return:
    """
    return getdate(showdate).strftime(timeformat)


def dateindaytimeformat(showdate):
    """
    Gibt einen String im daytimeformat von einem Datum zurück.
    :param showdate: Datum der Show
    :return: Datum als String in daytimeformat
    """
    return getdate(showdate).strftime(daytimeformat)


def getshowfromtoday(showdata, stream):
    """
    Erstellt den heutigen Sendeplan
    :param showdata: Sendeplandatei
    :param stream: Stream
    :return: Sendeplan von heute für den jeweiligen Stream als String
    """
    return getshowfromday(showdata, getdate(datetime.now().timestamp()).weekday(), stream)


def getshowfromtomorrow(showdata, stream):
    """
    Erstellt den morgigen Sendeplan
    :param showdata: Sendeplandatei
    :param stream: Stream
    :return: Sendeplan von morgen für den jeweiligen Stream als String
    """
    tomorrow = datetime.now() + timedelta(days=1)
    return getshowfromday(showdata, getdate(tomorrow.timestamp()).weekday(), stream)


def getshowfromday(showdata, date, stream):
    """
    Erstellt den Sendeplan von einem ausgewählten Datum
    :param showdata: Sendeplandatei
    :param date: Datum
    :param stream: Stream
    :return: Sendeplan von einem ausgewählten Datum für den jeweiligen Stream als String
    """
    now = datetime.now().date()
    result_date = now
    while result_date.weekday() != date:
        result_date += timedelta(days=1)
    reply = "%sShows am %s @ %s%s\n" % (emoji.info_button,wochentag[date],
                                        stream.capitalize(),emoji.info_button)
    showstring = ""
    for show in showdata:
        start = getdate(int(show["start "]))
        end = getdate(show["end"] - int(show["start "]))
        if start.date() == result_date <= end.date():
            start_string = getdateinstring(int(show["start "]))
            end_string = getdateinstring(show["end"] - int(show["start "]))
            showstring += createshowstring(show, start_string, end_string)
    if not showstring:
        reply += str('''%sKEINE SHOW VORHANDEN!''' % emoji.thumb_down)
        logger.debug("REPLY: " + reply)
        return reply
    else:
        reply += showstring
        logger.debug("REPLY: " + reply)
        return reply


def getdjnamebyshow(show):
    """
    Überprüft, ob der DJ seine WAO-ID mit seinem Telegrammaccount registriert hat.
    Wenn ja, wird sein Nutzername von Telegramm zurückgegeben.
    Wenn nicht gibt er den normalen DJ-Namen zurück.
    Funktioniert mit den Sendeplan-JSON-Dateien.
    :param show: Die dazugehörige Show
    :return: der resultierende Name als String
    """
    name = None
    users = getfile("users")
    for key, value in users.items():
        if value.get("wao_id") == show["user_id"]:
            name = "@" + value.get("user_name")
            logger.debug("WeAreOne-ID found. Telegram Chat ID: " + str(key))
    if not name:
        name = show["username"]
    return name


def getdjnamebyonair(dj, waoid):
    """
    Überprüft, ob der DJ seine WAO-ID mit seinem Telegrammaccount registriert hat.
    Wenn ja, wird sein Nutzername von Telegramm zurückgegeben.
    Wenn nicht gibt er den normalen DJ-Namen zurück.
    Funktioniert mit den OnAir-JSON-Dateien.
    :param dj: Der zu überprüfende dj
    :param waoid: Die zu überprüfende WAO-ID
    :return: Der resultierende Name als String
    """
    name = None
    users = getfile("users")
    for key, value in users.items():
        if value.get("wao_id") == waoid:
            name = "@" + value.get("user_name")
            logger.debug("WeAreOne-ID found. Telegram Chat ID: " + str(key))
    if not name:
        name = dj
    return name


def createshowstring(show, start, ende):
    """
    Erstellt einen String für eine Show.
    Wird benötigt für die Sendeplanmethode, um den Sendeplan als String zu erstellen.
    :param show:
    :param start: Startzeit als String
    :param ende: Endzeit als String
    :return: Show als String
    """
    name = getdjnamebyshow(show)

    showname = show["showname"]
    if not showname:
        return str('''%sShow by %s
%sZeit: %s - %s
''' % (emoji.microphone, name, emoji.alarm_clock, str(start), str(ende)))

    else:
        return str('''%sShow: \"%s\" by %s
%sZeit: %s - %s
''' % (emoji.microphone,show["showname"], name,emoji.alarm_clock, str(start), str(ende)))


def getstreamparameter(message):
    """
    Prüft, welcher Konfiguration bzw ob Streamparameter weitergegeben wurden.
    Dies wird in folgender Reihenfolge abgearbeitet und zurückgegeben:
    1. Nutzer hat einen Streamparameter nach dem Radiobefehl eingegeben. Der Wert wird zurückgegeben
    2. Falls 1. nicht wahr und der Nutzer für sich individuell über "/stream" einen Nutzerstreamgesetzt hat, wird dieser
    Wert zurückgegeben
    3. Falls 1. und 2. nicht wahr und die Gruppe hat einen Stream voreingestellt, wird dieser Wert zurückgegeben.
    4. Falls 1., 2. und 3. nicht wahr, gibt er einen leeren String zurück.
    :param message: Die vom Nutzer gesendete Nachricht
    :return: die Streams (siehe 1.-4.)
    """
    user = message.from_User
    uservalues = getfilevalue("users", user.chat_id)
    groupvalues = getfilevalue("groups", message.chat_id())
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
