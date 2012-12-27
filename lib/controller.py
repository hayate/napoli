#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webob import Request
from webob import Response

class Controller(object):
    def __init__(self):
        self.request = None
        self.response = Response()
