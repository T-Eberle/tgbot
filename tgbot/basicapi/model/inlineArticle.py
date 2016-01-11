# -*- coding: utf-8 -*-
__author__ = 'Thomas'

from tgbot.basicapi.model.inlineObject import InlineObject

class InlineArticle(InlineObject):

    def __init__(self,title,message_text,parse_mode=None,
                 disable_web_page_preview=None,url=None,hide_url=None,
                 description = None,thumb_url=None,thumb_width=None,thumb_height=None):
        self.type = "article"
        self.title = title
        self.message_text = message_text
        if url:
            self.url = url
        if hide_url:
            self.hide_url = hide_url
        if description:
            self.description = description
        if thumb_url:
            self.thumb_url = thumb_url
        if thumb_width:
            self.thumb_width = thumb_width
        if thumb_height:
            self.thumb_height = thumb_height
        super(InlineArticle, self).__init__("article",parse_mode=parse_mode,
                                          disable_web_page_preview=disable_web_page_preview)
