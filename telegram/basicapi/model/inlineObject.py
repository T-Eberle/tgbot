# -*- coding: utf-8 -*-
__author__ = 'Thomas'

import json
import uuid


class InlineObject:

    def __init__(self,type,parse_mode=None,disable_web_page_preview=None):

        self.type = type

        self.id = str(uuid.uuid4())

        if parse_mode:
            self.parse_mode = parse_mode
        if disable_web_page_preview:
            self.disable_web_page_preview = disable_web_page_preview
