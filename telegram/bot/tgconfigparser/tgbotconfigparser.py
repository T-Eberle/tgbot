__author__ = 'Thomas'
import sys
import pkg_resources

sys.path.append('/var/www/WeAreOne_Bot')

import configparser


class TGBotConfigParser:
    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        config = configparser.ConfigParser()
        data = pkg_resources.resource_filename("resources.config", self.file_name)
        config.read(data)
        return config


if __name__ == '__main__':
    config = TGBotConfigParser("server.ini")
    data = config.load()
    print(data.get("SSL_Config","ssl_key"))
