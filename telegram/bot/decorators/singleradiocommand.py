# -*- coding: utf-8 -*-
__author__ = 'Tommy'

import collections
from telegram.basicapi.commands import sendreply_one_keyboardmarkup,hide_keyboard
from telegram.bot.commands import getstreamparameter,getparameter
from telegram.tgredis import deleteconv,setconvcommand,getconvcommand
from telegram.tglogging import logger
import re
from resources import emoji

unsorted_radiostreams = {"tb": "technobase", "ht": "housetime", "hb": "hardbase", "trb": "trancebase", "ct": "coretime",
                         "clt": "clubtime"}
radiostreams = collections.OrderedDict(sorted(unsorted_radiostreams.items()))


def singleradiocommand(wrapped):
        """
        Methodenrumpf für alle Radiocommands.
        Da alle Radiobefehle Streams als Parameter benötigen, wird dieser hier direkt weitergegeben.
        Außerdem wird hier zwischen Befehlen unterschieden,
        die entweder nur eine oder mehrere Nachrichten verschicken können.
        Ein Sendeplanbefehl muss beispielsweise für jeden Stream eine Nachricht verschicken,
        wo es andererseits beim Listenerbefehl reicht wenn alle Streams in eine Nachricht gepackt werden.
        """
        def _wrapped(*args):
            regex = re.compile(r'(\b(ht|ct|clt|tb|hb|wao|all|coretime|housetime|technobase|trancebase|clubtime|hardbase)\b)')
            logger.debug("ARGS: " + str(args))
            obj = args[0]
            message = args[1]
            if getconvcommand(message)== wrapped.__name__ and message.text=="Cancel":
                hide_keyboard(message,message.chat_id(), emoji.warning+"Befehl \"/"+ wrapped.__name__+"\" abgebrochen.")
                deleteconv(message)
                return
            elif getconvcommand(message)== wrapped.__name__ and regex.search(message.text.lower()):
                parameter = message.text.lower()
                deleteconv(message)
            else:
                text = message.text
                chat = getstreamparameter(message)
                parameter = getparameter(text,chat).lower()
            try:
                reply = ""
                if "wao" in parameter or "all" in parameter:
                        for stream in radiostreams.values():
                            obj.radiostream = stream
                            values = wrapped(*args)
                            reply += values[1]
                        hide_keyboard(message,values[0], reply + "#%s" % wrapped.__name__)
                        deleteconv(message)
                elif not parameter or (not (any(radio in parameter.lower() for radio
                                                in list(radiostreams.values())) or any(radio in parameter.lower()
                                                                                       for radio
                                                                                       in list(radiostreams.keys()))))\
                        or parameter.lower() == "markup":
                    keyboard = [["Technobase","Housetime","Hardbase"],["Coretime","Clubtime","Trancebase"],["All"],["Cancel"]]
                    sendreply_one_keyboardmarkup(message,message.chat_id(),
                                                                   "\U0000274CBitte wähle einen Radiostream aus.\n/" +
                                                                   wrapped.__name__,keyboard)
                    setconvcommand(message, wrapped.__name__)
                else:
                    for radiostream in radiostreams.items():
                        if radiostream[0] in parameter.lower() or radiostream[1] in parameter:
                            obj.radiostream = radiostream[1]
                            values = wrapped(*args)
                            reply += values[1]
                    hide_keyboard(message, message.chat_id(), reply + "#%s" % wrapped.__name__)
                    deleteconv(message)
            except TypeError as typo:
                    logger.exception(typo)
                    hide_keyboard(message, message.chat_id(), "Witzbold.")
                    deleteconv(message)
        return _wrapped
