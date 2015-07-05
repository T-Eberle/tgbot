__author__ = 'Thomas'

from weareone.common.types.user import User
from weareone.common.types.audio import Audio


class Message:
    def __init__(self, message_id, from_user, date, chat, forward_from_user: User=None,
                 forward_date: int=None, reply_to_message=None, text=None, audio: Audio=None,
                 document=None, photo=None, sticker=None, video=None, contact=None, location=None,
                 new_chat_participant: User=None, left_chat_participant: User=None, new_chat_title=None,
                 new_chat_photo=None, delete_chat_photo=None, group_chat_created=None):
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
