# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.basicapi.model.inlineObject import InlineObject

class InlinePhoto(InlineObject):

    def __init__(self,photo_url,thumb_url=None,photo_width=None,
                 photo_height=None,title=None,description=None,caption=None,
                 message_text = None, parse_mode=None,disable_web_page_preview=None):
        self.photo_url = photo_url
        if thumb_url:
            self.thumb_url = thumb_url
        if photo_width:
            self.photo_width = photo_width
        if photo_height:
            self.photo_height = photo_height
        if title:
            self.title = title
        if description:
            self.description = description
        if caption:
            self.caption = caption
        if message_text:
            self.message_text = message_text

        super(InlinePhoto, self).__init__("photo",parse_mode=parse_mode,
                                          disable_web_page_preview=disable_web_page_preview)