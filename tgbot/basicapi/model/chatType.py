# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from tgbot.basicapi.model.base import Base


class ChatType(Base):
    def __createfromdata__(self, data):
        self.chat_id = data["id"]

    def __init__(self, data=None, chat_id=None):
        super().__init__()

