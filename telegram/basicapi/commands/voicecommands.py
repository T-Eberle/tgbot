__author__ = 'Bosner'

from telegram.basicapi.model.message import Message
from telegram.basicapi.commands import dosomethingwithfile


class VoiceController:
    def __init__(self, message: Message=None):
        self.message = message

    @staticmethod
    def sendvoice(chat_id, voice,complete_path=None):
        dosomethingwithfile(method_name="sendVoice",file_id="voice",
        filename=voice,path="resources.voice",chat_id=chat_id,complete_path=complete_path)

if __name__ == "__main__":
    VoiceController.sendvoice(-27587386,"alarm.ogg")
