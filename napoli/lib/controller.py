#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webob import Request
from webob import Response

class Controller(object):
    def __init__(self):
        self.request = None
        self.response = None

    @property
    def is_post(self):
        return 'POST' == self.method

    @property
    def is_get(self):
        return 'GET' == self.method

    @property
    def is_head(self):
        return 'HEAD' == self.method

    @property
    def is_ajax(self):
        """
        only works if X-Requested-With header is present and equal to XMLHttpRequest
        """
        return self.request.is_xhr

    @property
    def method(self):
        try:
            return self.request.method
        except:
            return None
