#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.singleton import Singleton
import settings


class Napoli(Singleton):
    def __init__(self):
        super(Napoli, self).__init__()
        if getattr(self, '__init', False):
            # do initialization here
            os.environ['APPPATH'] = settings.application

    def wsgi(self, environ, start_response):
        start_response('200 OK', [('Content-Type','text/html')])
        return 'Hello World!'

    def __call__(self, environ, start_response):
        return self.wsgi(environ, start_response)