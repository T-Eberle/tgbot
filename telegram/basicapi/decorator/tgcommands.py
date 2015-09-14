__author__ = 'Tommy'

from telegram.basicapi.commands.messagecommands import MessageController


def sendreply(replymessage):
    def wrapper(*args):
        message = args[1]
        chat_id = int(replymessage(*args)[0])
        MessageController.sendreply(message, chat_id, replymessage(*args)[1])

    return wrapper


def sendtext(textmessage):
    def _sendtext(*args):
        tuple = textmessage(*args)
        chat_id = int(tuple[0])
        MessageController.sendtext(chat_id, tuple[1])

    return _sendtext

# def sendStringasDoc(filemessage):
#     def wrapper(*args):
#         tuple=filemessage(*args)
#         chat_id=tuple[0]
#         file_name=
