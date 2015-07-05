__author__ = 'Thomas'

from weareone.common.types.chatType import ChatType


class GroupChat(ChatType):
    def __init__(self, chattype_id, title):
        self.id = chattype_id
        self.title = title
