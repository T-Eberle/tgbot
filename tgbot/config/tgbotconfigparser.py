# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import configparser

import pkg_resources


class TGBotConfigParser:
    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath= filepath
        self.config = configparser.ConfigParser()
        self.config._interpolation = configparser.ExtendedInterpolation()
        configdata = pkg_resources.resource_filename(filepath, filename)
        try:
            self.config.read_file(open(configdata, encoding="latin-1"), source=filename)
        except FileNotFoundError:
            self.filename = "basicconfig.ini"
            configdata = pkg_resources.resource_filename(self.filepath, self.filename)
            self.config.read_file(open(configdata, encoding="latin-1"), source=filename)

    def load(self):
        self.config = configparser.ConfigParser()
        self.config._interpolation = configparser.ExtendedInterpolation()
        configdata = pkg_resources.resource_filename(self.filepath, self.filename)
        self.config.read_file(open(configdata, encoding="latin-1"), source=self.filename)
        return self.config
