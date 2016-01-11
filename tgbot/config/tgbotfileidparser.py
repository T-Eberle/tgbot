# -*- coding: utf-8 -*-
__author__ = 'Thomas Eberle'

import configparser
import pkg_resources


class TGBotFileIDParser:
    def __init__(self,filepath):
        self.config = configparser.ConfigParser()
        self.config._interpolation = configparser.ExtendedInterpolation()
        data = pkg_resources.resource_filename(filepath, "file_ids.ini")
        self.config.read_file(open(data, encoding="latin-1"), source="file_ids.ini")

    def load(self,filepath):
        self.config = configparser.ConfigParser()
        self.config._interpolation = configparser.ExtendedInterpolation()
        data = pkg_resources.resource_filename(filepath, "file_ids.ini")
        self.config.read_file(open(data, encoding="latin-1"), source="file_ids.ini")
        return self.config
