# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from telegram.basicapi.model.inlineObject import InlineObject

class InlineGif(InlineObject):

    def __init__(self,gif_url,thumb_url,gif_width=None,gif_height=None,title=None,caption=None,
                 message_text=None,parse_mode=None,disable_web_page_preview=None):
        self.gif_url = gif_url
        self.thumb_url = thumb_url
        if gif_width:
            self.gif_width = gif_width
        if gif_height:
            self.gif_height = gif_height
        if title:
            self.title = title
        if caption:
            self.caption = caption
        if message_text:
            self.message_text = message_text


        super(InlineGif, self).__init__("gif",parse_mode=parse_mode,
                                          disable_web_page_preview=disable_web_page_preview)