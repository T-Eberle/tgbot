__author__ = 'Thomas'

from weareone.model import ChatType


class User(ChatType):
    def __init__(self, first_name, last_name, username):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
