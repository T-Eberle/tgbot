__author__ = 'Thomas'

from telegram.bot.basicapi.commands.messagecommands import MessageController
from telegram.bot.basicapi.commands.stickercommands import StickerController
from telegram.bot.tglogging.TGLogger import logger
from telegram.bot.config.tgbotfileidparser import TGBotFileIDParser

radiocommands = ["listener", "dj", "now", "sendeplan","housetime","technobase","hardbase","trancebase","coretime","clubtime"]

config = TGBotFileIDParser()
data = config.load()


def parseradiocommands(message, text):
    logger.debug("/"+text+" command recognized.")
    if (text == radiocommands[0]):
        listener(message)
    elif (text == radiocommands[1]):
        dj(message)
    elif (text == radiocommands[2]):
        now(message)
    elif (text == radiocommands[3]):
        sendeplan(message)
    elif (text == radiocommands[4]):
        housetime(message)
    elif (text == radiocommands[5]):
        technobase(message)
    elif (text == radiocommands[6]):
        hardbase(message)
    elif (text == radiocommands[7]):
        trancebase(message)
    elif (text == radiocommands[8]):
        coretime(message)
    elif (text == radiocommands[9]):
        clubtime(message)


def dj(message):
    MessageController.sendreply(message, message.chat_id(),
                                "\U0001F3A4" + "Aktueller DJ: DJ Superstar \n #dj")


def now(message):
    MessageController.sendreply(message, message.chat_id(),
                                "\U0001F3A4" + "Aktueller DJ: DJ Superstar \n" +
                                "\U0001F4E2" + "Showname: Pusteblume #now")


def listener(message):
    MessageController.sendreply(message, message.chat_id(),
                                "\U0001F4E1" + "Aktueller Listeneranzahl: 1 \n #listener" +
                                "Du Lappen!\U0001F4A9")


def sendeplan(message):
    MessageController.sendreply(message, message.chat_id(),
                                "Der Sendeplan ist leer.... \n" +
                                "Ich bin enttaeuscht!#sendeplan")
def housetime(message):
    StickerController.sendstickerwithid(message.chat_id(),data.get("file_ids","housetime"))

def technobase(message):
    StickerController.sendstickerwithid(message.chat_id(),data.get("file_ids","technobase"))

def hardbase(message):
    StickerController.sendstickerwithid(message.chat_id(),data.get("file_ids","hardbase"))

def trancebase(message):
    StickerController.sendstickerwithid(message.chat_id(),data.get("file_ids","trancebase"))

def coretime(message):
    StickerController.sendstickerwithid(message.chat_id(),data.get("file_ids","coretime"))

def clubtime(message):
    StickerController.sendstickerwithid(message.chat_id(),data.get("file_ids","clubtime"))


