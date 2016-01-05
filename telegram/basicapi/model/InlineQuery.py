# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

from telegram.basicapi.model.user import User

class InlineQuery:

    def __createfromdata__(self, data):
        self.data = data

        self.id = data["id"]

        self.from_User = User(data=data["from"])

        self.query = data["query"]

        self.offset = data["offset"]

    def __init__(self, data=None,id=None,from_User=None,query=None,offset=None):
        if data:
            self.__createfromdata__(data)
        else:
            self.id = id
            self.from_User = from_User
            self.query = query
            self.offset = offset