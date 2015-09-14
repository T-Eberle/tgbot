__author__ = 'Thomas Eberle'

from telegram.basicapi.model.chatType import ChatType
from telegram.tglogging import *


class User(ChatType):
    def getchatid(self):
        return self.chat_id

    def __createfromdata__(self, data):
        super(User, self).__createfromdata__(data)
        try:
            self.first_name = data["first_name"]
        except KeyError:
            self.first_name = ""
            logger.debug("No first name available.")
        try:
            self.last_name = ""
            self.last_name = data["last_name"]
        except KeyError:
            logger.debug("No last name available.")
        try:
            self.username = data["username"]
        except KeyError:
            self.username = ""
            logger.debug("No username available.")

    def __init__(self, data=None, chat_id=None, first_name=None, last_name=None, username=None):
        if data:
            super(User, self).__init__(data=data, chat_id=chat_id)
        else:
            self.first_name = first_name
            self.last_name = last_name
            self.username = username
