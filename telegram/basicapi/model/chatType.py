__author__ = 'Thomas Eberle'

from telegram.basicapi.model.base import Base


class ChatType(Base):
    def __createfromdata__(self, data):
        self.chat_id = data["id"]

    def __init__(self, data=None, chat_id=None):
        if data:
            self.__createfromdata__(data)
        else:
            self.chat_id = chat_id
