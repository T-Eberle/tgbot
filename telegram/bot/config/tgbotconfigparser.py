__author__ = 'Thomas'

import configparser
import pkg_resources


class TGBotConfigParser:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config._interpolation = configparser.ExtendedInterpolation()
        data = pkg_resources.resource_filename("resources.config", "config.ini")
        self.config.read_file(open(data,encoding="latin-1"),source="config.ini")

    def load(self):
        self.config = configparser.ConfigParser()
        self.config._interpolation = configparser.ExtendedInterpolation()
        data = pkg_resources.resource_filename("resources.config", "config.ini")
        self.config.read_file(open(data,encoding="latin-1"),source="config.ini")
        return self.config


if __name__ == '__main__':
    print(dir)
    config = TGBotConfigParser("config.ini")
    data = config.load()
    print(data.get("basics", "address"))
    print(config.config.get("tgapi", "bot_link"))
    print(data.get("tgapi", "bot_link"))
