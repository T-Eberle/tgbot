# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import configparser
import pkg_resources
import resources.config


class TGBotConfigParser:
    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config._interpolation = configparser.ExtendedInterpolation()
        configdata = pkg_resources.resource_filename("resources.config", filename)
        try:
            self.config.read_file(open(configdata, encoding="latin-1"), source=filename)
        except FileNotFoundError:
            self.filename = "basicconfig.ini"
            configdata = pkg_resources.resource_filename("resources.config", self.filename)
            self.config.read_file(open(configdata, encoding="latin-1"), source=filename)

    def load(self):
        self.config = configparser.ConfigParser()
        self.config._interpolation = configparser.ExtendedInterpolation()
        configdata = pkg_resources.resource_filename("resources.config", self.filename)
        self.config.read_file(open(configdata, encoding="latin-1"), source=self.filename)
        return self.config
