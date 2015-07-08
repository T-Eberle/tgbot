__author__ = 'Thomas'

from weareone.model.message import Message
from weareone.common.weAreOneParameters import bot_link, \
     sendMessage_Method
from weareone.controllers import HTTPRequestController


class MessageController:
    def __init__(self, message:Message=None):
        self.message = message

    def sendMessage(chat_id,text):
        url= bot_link + sendMessage_Method
        values ={"chat_id": -27587386,"text": text}

        print(HTTPRequestController.requestWithValues(None, url, values))

