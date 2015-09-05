__author__ = 'Thomas Eberle'

from telegram.basicapi.model.base import Base


class Audio(Base):
    def __init__(self, file_id):
        super().__init__()
        self.file_id = file_id
