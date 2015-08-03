__author__ = 'Thomas Eberle'

from telegram.bot.config.tgbotfileidparser import TGBotFileIDParser
from telegram.bot.tglogging.TGLogger import logger
from telegram.bot.basicapi.commands.stickercommands import StickerController
from telegram.bot.basicapi.commands.messagecommands import MessageController

entertaincommands = ["genius","me gusta","halt stop", "halt, stop","halt,stop"]

config = TGBotFileIDParser()
data = config.load()


def parseentertaintext(message):
    if (entertaincommands[0] in message.text.lower()):
        logger.debug("\"" + entertaincommands[0] + "\"-text recognized.")
        genius(message)
    elif (entertaincommands[1] in message.text.lower()):
        logger.debug("\"" + entertaincommands[1] + "\"-text recognized.")
        megusta(message)
    elif (entertaincommands[2] in message.text.lower() or
          entertaincommands[3] in message.text.lower() or
          entertaincommands[4] in message.text.lower()):
        logger.debug("\"" + entertaincommands[3] + "\"-text recognized.")
        haltstop(message)

def genius(message):
    StickerController.sendstickerwithid(message.chat_id(), data.get("file_ids", "genius"))
def megusta(message):
    StickerController.sendstickerwithid(message.chat_id(), data.get("file_ids", "megusta"))
def haltstop(message):
    MessageController.sendreply(message,message.chat_id(),"JETZT REDE ICH!\n"+
                                "https://www.youtube.com/watch?v=C1fCJvgNDow")
