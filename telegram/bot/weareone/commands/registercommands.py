__author__ = 'Thomas'


registercommands = ["register","unregister"]


def parseregistercommands(message,text):
    logger.debug("/"+text+" command recognized.")
    if (text == registercommands[0]):
        register(message)
    elif (text == registercommands[1]):
        unregister(message)


def register(message):
    pass

def unregister(message):
    pass
