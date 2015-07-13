__author__ = 'Thomas'
import sys
path = '/usr/tgbot'
sys.path.append(path)

from telegram.bot.server.telegrambothttpsserver import start


if __name__ == '__main__':
   start()
