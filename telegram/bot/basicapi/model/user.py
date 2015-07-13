__author__ = 'Thomas'

from telegram.bot.basicapi.model.chatType import ChatType


class User(ChatType):
    def getchatid(self):
        return self.chat_id

    def __createfromdata__(self,data):
        super(User, self).__createfromdata__(data)
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.username=data["username"]
    def __init__(self,data=None,chat_id=None, first_name=None, last_name=None, username=None):
        if data:
            super(User, self).__init__(data=data,chat_id=chat_id)
        else:
            self.first_name = first_name
            self.last_name = last_name
            self.username = username
