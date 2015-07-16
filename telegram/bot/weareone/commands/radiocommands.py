__author__ = 'Thomas'

from telegram.bot.basicapi.commands.messagecommands import MessageController
from telegram.bot.tglogging.TGLogger import logger

radiocommands = ["listener", "dj", "now", "sendeplan"]


def parseradiocommands(message, text):
    if (text == radiocommands[0]):
        listener(message)
    elif (text == radiocommands[1]):
        dj(message)
    elif (text == radiocommands[2]):
        now(message)
    elif (text == radiocommands[3]):
        sendeplan(message)


def dj(message):
    logger.debug("/dj command recognized.")
    MessageController.sendreply(message, message.chat_id(),
                                "\U0001F3A4" + "Aktueller DJ: DJ Superstar \n #dj")


def now(message):
    logger.debug("/now command recognized.")
    MessageController.sendreply(message, message.chat_id(),
                                "\U0001F3A4" + "Aktueller DJ: DJ Superstar \n" +
                                "\U0001F4E2" + "Showname: Pusteblume #now")


def listener(message):
    logger.debug("/listener command recognized.")
    MessageController.sendreply(message, message.chat_id(),
                                "\U0001F4E1" + "Aktueller Listeneranzahl: 1 \n #listener" +
                                "Du Lappen!\U0001F4A9")


def sendeplan(message):
    logger.debug("/sendeplan command recognized.")
    MessageController.sendreply(message, message.chat_id(),
                                "Der Sendeplan ist leer.... \n" +
                                "Ich bin enttaeuscht!#sendeplan")

