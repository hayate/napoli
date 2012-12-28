#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.controller import Controller


class Index(Controller):

    def index(self, *arg):
        return 'the arg is: {0}'.format(arg)