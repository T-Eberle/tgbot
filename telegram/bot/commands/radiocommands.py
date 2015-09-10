# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'


from telegram.bot.commands import *
from telegram.config.tgbotfileidparser import TGBotFileIDParser
from telegram.config.waoapiparser import WAOAPIParser
from telegram.tgredis import *
from resources import emoji
from telegram.bot.decorators.multiRadioCommand import multiRadioCommand
from telegram.bot.decorators.singleRadioCommand import singleRadioCommand
from datetime import datetime,timedelta

waoParser = WAOAPIParser("housetime_onAir")

fileconfig = TGBotFileIDParser()
filedata = fileconfig.load()


class RadioCommands:
    def __init__(self):
        self.chat = None
        self.radiostream = ""



    @multiRadioCommand
    def gestern(self,message):
        return getshowfromday(None,self.radiostream)

    @multiRadioCommand
    def montag(self,message):
        return getshowfromday(0, self.radiostream)

    @multiRadioCommand
    def dienstag(self,message):
        return getshowfromday(1, self.radiostream)

    @multiRadioCommand
    def mittwoch(self,message):
        return getshowfromday(2, self.radiostream)

    @multiRadioCommand
    def donnerstag(self,message):
        return getshowfromday(3, self.radiostream)

    @multiRadioCommand
    def freitag(self,message):
        return getshowfromday(4, self.radiostream)

    @multiRadioCommand
    def samstag(self,message):
        return getshowfromday(5, self.radiostream)

    @multiRadioCommand
    def sonntag(self,message):
        return getshowfromday(6, self.radiostream)

    @multiRadioCommand
    def heute(self,message):
        return getshowfromtoday(self.radiostream)

    @multiRadioCommand
    def morgen(self,message):
        return getshowfromtomorrow(self.radiostream)

    @singleRadioCommand
    def next(self,message):
        return nextshow(self.radiostream)

    @singleRadioCommand
    def lastshow(self,message):
        return lastshow(self.radiostream)

    @singleRadioCommand
    def track(self,message):
        try:
            artist = WAOAPIParser.nowartist(self.radiostream)
            track =WAOAPIParser.nowtrack(self.radiostream)
            release =WAOAPIParser.nowrelease(self.radiostream)
            release_string =""
            if release!="0":
                release_string =str("Check: http://www.technobase.fm/release/%s\n" % release)
            return str("%sAktueller Track @ %s: %s - %s\n"% (emoji.musical_note,self.radiostream.capitalize(), artist, track))\
                   + release_string

        except KeyError as error:
            logger.exception(error)
            return str('''%sKein DJ ON AIR @ %s!
''' % (emoji.thumb_down,self.radiostream.capitalize()))

    @singleRadioCommand
    def dj(self,message):
        try:
            dj = WAOAPIParser.now(self.radiostream,"dj")
            djid = str(WAOAPIParser.now(self.radiostream,"djid"))
            return str('''%sAktueller DJ @ %s: %s
''' % (emoji.microphone,self.radiostream.capitalize(), getdjnamebyonair(dj, djid)))
        except KeyError:
            return str('''%sKein DJ ON AIR @ %s!
''' % (emoji.thumb_down,self.radiostream.capitalize()))


    @singleRadioCommand
    def listener(self,message):
        listener = waoParser.gettrayelement(self.radiostream + "_onAir", "listener")
        return str('''%s*Aktuelle Listeneranzahl* @ _%s_: %s
''' % (emoji.satellite,self.radiostream.capitalize(), listener))

    @singleRadioCommand
    def now(self,message):
        try:
            WAOAPIParser.now(self.radiostream,"playlist")
            return str('''%sAktuelle Show-Info @ %s%s
%sKein DJ ON AIR!
''' % (emoji.info_button,self.radiostream.capitalize(),emoji.info_button,emoji.thumb_down))
        except KeyError:
            dj = WAOAPIParser.now(self.radiostream,"dj")
            djid = str(WAOAPIParser.now(self.radiostream, "djid"))
            show = WAOAPIParser.now(self.radiostream,"show")
            style = WAOAPIParser.now(self.radiostream,"style")
            start = WAOAPIParser.nowstart_string(self.radiostream)
            end = WAOAPIParser.nowend_string(self.radiostream)
            if dj:
                return str('''%sAktuelle Show-Info @ %s%s
%sDJ: %s
%sShowname: %s
%sStyle: %s
%sUhrzeit: %s bis %s
''' % (emoji.info_button,self.radiostream.capitalize(),emoji.info_button,emoji.microphone,
       getdjnamebyonair(dj, djid),emoji.loudspeaker, show,emoji.headphone, style,emoji.alarm_clock, start, end))

    @singleRadioCommand
    def tracklist(self,message):
        waoapi = WAOAPIParser(stream=self.radiostream)
        tracks = waoapi.loadwaoapitracklist(count=20, upcoming=True)

        text = "\n\nTracklist für %s: \n" % self.radiostream.capitalize()
        result = ""
        for track in tracks:
            start_timestamp = track[waodata.get("waoapi-tracklist", "playtime")]
            start_date_string = WAOAPIParser.correctdate_timeformat(int(start_timestamp), format="%a %H:%M")
            start_date = WAOAPIParser.correcdate(start_timestamp)
            now = datetime.now()
            now_rounded = now - timedelta(minutes=now.minute)
            if now_rounded - start_date <= timedelta(hours=1) and start_date < now_rounded:
                artist = track[waodata.get("waoapi-tracklist", "artist")]
                title = track[waodata.get("waoapi-tracklist", "title")]

                result += start_date_string + ": " + artist + " - " + title + "\n"
        if not result:
            return str('Keine Tracklist verfügbar für %s' % self.radiostream.capitalize())
        return text + result
