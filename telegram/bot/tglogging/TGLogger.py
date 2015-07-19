__author__ = 'Thomas'

from logging.handlers import *
import logging.handlers

logger = logging.getLogger("TG BOT")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream = logging.StreamHandler()
stream.setFormatter(formatter)

logger.addHandler(stream)

#syslog = SysLogHandler(address="/dev/log")
#syslog.setFormatter(formatter)

#logger.addHandler(syslog)
