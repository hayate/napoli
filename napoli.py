#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from webob import Request
from lib.singleton import Singleton
from lib.dispatcher import Dispatcher
from lib.router import Router
from lib.router import Routes
from configs import routes
import settings


class Napoli(Singleton):
    def __init__(self):
        super(Napoli, self).__init__()
        if getattr(self, '__init', False):
            # do initialization here
            os.environ['APPPATH'] = settings.application
            sys.path.append(os.path.dirname(os.environ['APPPATH']))
            self.routes = Routes(routes.routes)

    def wsgi(self, environ, start_response):
        """
        All per request initialization goes here
        """
        # initialize router
        router = Router(self.routes)
        router.route(environ['PATH_INFO'])
        # dispatch
        dispatcher = Dispatcher(Request(environ), router)
        res = dispatcher.dispatch()
        return res

    def __call__(self, environ, start_response):
        res = self.wsgi(environ, start_response)
        return res(environ, start_response)
