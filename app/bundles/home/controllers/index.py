#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.controller import Controller


class Index(Controller):

    def index(self):
        return __file__