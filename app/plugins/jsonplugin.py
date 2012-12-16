#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from webob import Response
from json import JSONEncoder
from functools import wraps
from lib.plugins import Plugin


class JsonPlugin(Plugin):
    def __init__(self):
        super(JsonPlugin, self).__init__('json')
        self.skipkeys = False
        self.ensure_ascii = True
        self.check_circular = True
        self.allow_nan = True
        self.cls = JSONEncoder
        self.indent = None
        self.separators =  (',', ':')
        self.encoding = 'UTF-8'

    def run(self, callback):
        @wraps(callback)
        def wrapper(*a, **kw):
            # call controller method
            obj = callback(*a, **kw)
            try:
                # create response
                res = Response(content_type='application/json')
                # encode into json
                res.json = json.dumps(obj, skipkeys=self.skipkeys,
                                 ensure_ascii=self.ensure_ascii,
                                 check_circular=self.check_circular,
                                 allow_nan=self.allow_nan,
                                 cls=self.cls,
                                 indent=self.indent,
                                 separators=self.separators,
                                 encoding=self.encoding)
                # return json response
                return res
            except TypeError:
                # obj is not json serializable,
                # we assume is webob.Response
                # and return it
                return obj

        return wrapper

    def setup(self, skipkeys=False, ensure_ascii=True, check_circular=True,allow_nan=True,
              cls=JSONEncoder, indent=None, separators=(',', ':'), encoding='UTF-8'):
        self.skipkeys = skipkeys
        self.ensure_ascii = ensure_ascii
        self.check_circular = check_circular
        self.allow_nan = allow_nan
        self.cls = cls
        self.indent = indent
        self.separators = separators
        self.encoding = encoding
