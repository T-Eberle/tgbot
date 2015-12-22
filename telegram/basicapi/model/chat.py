__author__ = 'Tommy'

from telegram.basicapi.model.base import Base

class Chat(Base):
    def __createfromdata__(self,data):
        self.data = data

        self.chattype = data["type"]

        self.chat_id = data["id"]

        if self.chattype == "private":
            if data["username"]:
                self.username = data["username"]
            self.first_name = data["first_name"]
            self.last_name = data["last_name"]
        elif self.chattype == "group":
            self.title = data["title"]
        elif self.chattype == "channel":
            if data["username"]:
                self.username = data["username"]
            self.title = data["title"]



    # id 	Integer 	Unique identifier for this chat, not exceeding 1e13 by absolute value
    # type 	String 	Type of chat, can be either “private”, or “group”, or “channel”
    # title 	String 	Optional. Title, for channels and group chats
    # username 	String 	Optional. Username, for private chats and channels if available
    # first_name 	String 	Optional. First name of the other party in a private chat
    # last_name 	String 	Optional. Last name of the other party in a private chat

    def __init__(self, data=None,chattype = None,title=None,username=None,first_name=None,last_name=None):

        if data:
            self.__createfromdata__(data)
        else:
            self.chattype = chattype
            if self.chattype == "private":
                if username:
                    self.username = username
                self.first_name = first_name
                self.last_name = last_name
            elif self.chattype == "group":
                self.title = title
            elif self.chattype == "channel":
                if username:
                    self.username = username
                self.title = title


