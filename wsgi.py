# -*- coding: utf-8 -*-
__author__ = 'Tommy'
import sys
import locale
import json

from telegram import activateBot

path = '/home/tgbot/telegrambot'
sys.path.append(path)

def application(environ,start_response):
    locale.setlocale(locale.LC_ALL,"de_DE.UTF8")
    start_response('200 OK',[('Content-Type','text/html')])

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    if request_body_size != 0:
        request_body = environ['wsgi.input'].read(request_body_size)
        obj = json.loads(request_body.decode('utf-8'))
        activateBot(obj)
    return b''