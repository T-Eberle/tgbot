__author__ = 'Tommy Elroy'

import datetime

from weareone.common.controllers.botapi.messagecontroller import *

str = "\u231A Auf meiner Uhr ist es "+datetime.datetime.now().time().isoformat()+". \u231A"
chat_id = -27587386

MessageController.sendMessage(chat_id,str)
#MessageController.sendMessage(str)





