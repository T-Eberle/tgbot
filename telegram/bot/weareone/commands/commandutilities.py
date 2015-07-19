__author__ = 'Thomas'

import re

def getparameter(text):
    replaced = re.sub(r'/(\w)*',"",text)
    return replaced.replace(" ","")
