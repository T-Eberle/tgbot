# -*- coding: utf-8 -*-
__author__ = 'Tommy'

import collections
from telegram.basicapi.commands.messagecommands import MessageController
from telegram.bot.commands import getstreamparameter,getparameter
from telegram.tgredis import deleteconv,addtoconv
from telegram.tglogging import logger

unsorted_radiostreams = {"tb": "technobase", "ht": "housetime", "hb": "hardbase", "trb": "trancebase", "ct": "coretime",
                         "clt": "clubtime"}
radiostreams = collections.OrderedDict(sorted(unsorted_radiostreams.items()))

def singleRadioCommand(wrapped):
        """
        Methodenrumpf für alle Radiocommands.
        Da alle Radiobefehle Streams als Parameter benötigen, wird dieser hier direkt weitergegeben.
        Außerdem wird hier zwischen Befehlen unterschieden,
        die entweder nur eine oder mehrere Nachrichten verschicken können.
        Ein Sendeplanbefehl muss beispielsweise für jeden Stream eine Nachricht verschicken,
        wo es andererseits beim Listenerbefehl reicht wenn alle Streams in eine Nachricht gepackt werden.
        """
        def _wrapped(*args):
            logger.debug("ARGS: "+str(args))
            obj = args[0]
            message =args[1]
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
                        MessageController.hide_Keyboard(message,values[0], reply + "#%s" % wrapped.__name__)
                        deleteconv(message)
                elif not parameter or (not (any(radio in parameter.lower() for radio in list(radiostreams.values())) or any(
                            radio in parameter.lower() for radio in list(radiostreams.keys()))))or parameter.lower()=="markup":
                    keyboard= [["Technobase","Housetime","Hardbase"],["Coretime","Clubtime","Trancebase"]]
                    MessageController.sendreply_one_keyboardmarkup(message,message.chat_id(),
                                                    "\U0000274CBitte wähle einen Radiostream aus.\n/"
                                                                   + wrapped.__name__
                                                    ,keyboard)
                    addtoconv(message,"/"+wrapped.__name__)
                else:
                    for radiostream in radiostreams.items():
                        if radiostream[0] in parameter.lower() or radiostream[1] in parameter:
                            obj.radiostream=radiostream[1]
                            values = wrapped(*args)
                            reply += values[1]
                    MessageController.hide_Keyboard(message, message.chat_id(), reply + "#%s" % wrapped.__name__)
                    deleteconv(message)
            except TypeError as typo:
                    logger.exception(typo)
                    MessageController.hide_Keyboard(message, message.chat_id(), "Witzbold.")
                    deleteconv(message)
        return _wrapped