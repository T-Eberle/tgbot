# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'


class Video:
    def __init__(self, file_id, width, height, duration, thumb, mime_type=None, file_size=None, caption=None):
        self.file_id = file_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.mime_type = mime_type
        self.file_size = file_size
        self.caption = caption
