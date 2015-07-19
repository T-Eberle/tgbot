__author__ = 'Thomas'

from telegram.bot.config.tgbotfileidparser import TGBotFileIDParser
from telegram.bot.tglogging.TGLogger import logger
from telegram.bot.basicapi.commands.stickercommands import StickerController

entertaincommands = ["genius","me gusta"]

config = TGBotFileIDParser()
data = config.load()


def parseentertaintext(message):
    if (entertaincommands[0] in message.text.lower()):
        logger.debug("\"" + entertaincommands[0] + "\"-text recognized.")
        genius(message)
    elif (entertaincommands[1] in message.text.lower()):
        logger.debug("\"" + entertaincommands[1] + "\"-text recognized.")
        megusta(message)

def genius(message):
    StickerController.sendstickerwithid(message.chat_id(), data.get("file_ids", "genius"))
def megusta(message):
    StickerController.sendstickerwithid(message.chat_id(), data.get("file_ids", "megusta"))
