# -*- coding: utf-8 -*-
__author__ = 'Thomas'

import inspect
from telegram.tglogging import logger


def parseinline(inline,args):
    query = inline.query

    if args:
        for obj in args:
            if inspect.getmembers(obj):
                for method in inspect.getmembers(obj):
                    if query.lower() == method[0]:
                        logger.info(query + " command recognized.")
                        getattr(obj,method[0])(inline)