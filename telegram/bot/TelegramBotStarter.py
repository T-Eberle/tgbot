__author__ = 'Thomas'
import sys
path = '/usr/tgbot/'
sys.path.append(path)

from telegram.bot.tglogging.TGLogger import logger
from telegram.bot.server.telegrambothttpsserver import start_pipe


from telegram.bot.server.telegrambothttpsserver import start

if __name__ == '__main__':
    logger.info("Main method initiated.")
    start_pipe()
