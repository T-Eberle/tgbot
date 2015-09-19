__author__ = 'Tommy'

from telegram.basicapi.commands import sendreply, sendtext


def reply(replymessage):
    def wrapper(*args):
        values = replymessage(*args)
        message = args[1]
        chat_id = int(values[0])
        sendreply(message, chat_id, values[1])

    return wrapper


def text(textmessage):
    def _sendtext(*args):
        tuple = textmessage(*args)
        chat_id = int(tuple[0])
        sendtext(chat_id, tuple[1])

    return _sendtext

# def sendStringasDoc(filemessage):
#     def wrapper(*args):
#         tuple=filemessage(*args)
#         chat_id=tuple[0]
#         file_name=
