__author__ = 'Tommy Elroy'

from telegram.bot.basicapi.commands.messagecommands import MessageController
from telegram.bot.basicapi.model.message import Message
from telegram.bot.basicapi.model.groupChat import GroupChat
from telegram.bot.basicapi.model.user import User
from telegram.bot.basicapi.model.chatType import ChatType
import telegram.bot.weareone.parser.messageparser as messageparser


class WeAreOneBot:
    def activateBot(data):
        message = Message(data=data)

        messageparser.parseMessage(message)

