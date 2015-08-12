__author__ = 'Thomas Eberles'

from telegram.basicapi.model.chatType import ChatType


class GroupChat(ChatType):
    def getchatid(self):
        return self.chat_id

    def __createfromdata__(self, data):
        self.title =data["title"]
        super(GroupChat, self).__createfromdata__(data)

    def __init__(self, data=None, chat_id=None, title=None):
        self.title = title
        super(GroupChat, self).__init__(data=data,chat_id=chat_id)
