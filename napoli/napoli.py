#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from webob import Request
from lib.singleton import Singleton
from lib.dispatcher import Dispatcher
from lib.router import Router
from lib.router import Routes
from lib.config import Config
from lib.plugins import Plugins
from lib.logger import Log


class Napoli(Singleton):
    def __init__(self):
        super(Napoli, self).__init__()
        if getattr(self, '__init', False):
            # do initialization here
            self.config = Config.get_instance()
            os.environ['APPPATH'] = self.config.application
            sys.path.append(os.path.dirname(os.environ['APPPATH']))
            self.log = Log()
            self.plugins = Plugins()
            self._load_plugins()
            self.routes = Routes()

    def _load_plugins(self):
        try:
            for name in self.config.plugins['default']:
                self.plugins.install(name)
        except KeyError as ex:
            self.log.debug(ex)
        except Exception as ex:
            self.log.exception(ex)


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
