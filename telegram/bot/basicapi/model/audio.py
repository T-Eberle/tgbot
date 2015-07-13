__author__ = 'Thomas'

from telegram.bot.basicapi.model.base import Base


class Audio(Base):
    def __init__(self, file_id):
        self.file_id = file_id
