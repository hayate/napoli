#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from singleton import Singleton
import configs.devel


class Config(Singleton):
    def __init__(self, module):
        """
        module (str): name of a python module containing configuration parameters
        """
        if getattr(self, '__init', False):
            # do initialization here
            segs = module.rsplit('.')
            name = segs.pop() if len(segs) > 1 else None
            if name:
                self.__data = __import__(module, fromlist=[name])
            else:
                self.__data = __import__(module)

    def __getattr__(self, name):
        return getattr(self.__data, name, None)

    def __getitem__(self, name):
        return getattr(self.__data, name, None)

    def __contains__(self, name):
        return hasattr(self.__data, name)
