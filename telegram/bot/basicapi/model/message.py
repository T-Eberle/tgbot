__author__ = 'Thomas'

from telegram.bot.basicapi.model.user import User
from telegram.bot.basicapi.model.audio import Audio
from telegram.bot.basicapi.model.base import Base
from telegram.bot.basicapi.model.chatType import ChatType
from telegram.bot.basicapi.model.groupChat import GroupChat


class Message(Base):
    def chat_id(self):
        return self.chat.getchatid()

    def __createfromdata__(self, data):
        # MESSAGE ID
        self.message_id = data["message_id"]

        # DATE
        self.date = data["date"]

        # USER
        user = data["from"]
        self.from_User = User(data=user)

        # CHAT
        chat = data["chat"]
        if "title" in chat:
            self.chat = GroupChat(data=chat)
        else:
            self.chat = User(data=chat)

        # self.forward_date = data["forward_date"]
        if "text" in data:
            self.text = data["text"]
        # self.new_chat_title = data["new_chat_title"]

    def __init__(self, data=None, message_id=None, from_user=None, date=None, chat=None, forward_from_user: User=None,
                 forward_date: int=None, reply_to_message=None, text=None, audio: Audio=None,
                 document=None, photo=None, sticker=None, video=None, contact=None, location=None,
                 new_chat_participant: User=None, left_chat_participant: User=None, new_chat_title=None,
                 new_chat_photo=None, delete_chat_photo=None, group_chat_created=None):
        if data:
            self.__createfromdata__(data["message"])

        else:
            self.message_id = message_id

            self.from_User = from_user

            self.date = date

            self.chat = chat

            self.forward_from_User = forward_from_user

            self.forward_Date = forward_date

            self.reply_to_message = reply_to_message

            self.text = text

            self.audio = audio

            self.document = document

            self.photo = photo

            self.sticker = sticker

            self.video = video

            self.contact = contact

            self.location = location

            self.new_chat_participant = new_chat_participant

            self.left_chat_participant = left_chat_participant

            self.new_chat_title = new_chat_title

            self.new_chat_photo = new_chat_photo

            self.delete_chat_photo = delete_chat_photo

            self.group_chat_created = group_chat_created
