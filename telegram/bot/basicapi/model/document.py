__author__ = 'Thomas'


class Document:
    def __init__(self, file_id, thumb, file_name, mime_type, file_size):
        self.file_id = file_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
