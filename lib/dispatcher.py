#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import importlib
import inspect
from webob import Response


class Dispatcher(object):
    def __init__(self, request, router):
        self._request = request
        self._router = router
        self._res = Response()

    def dispatch(self):
        action = self.get_action()

        res = action(*self._router.args())
        if not res:
            self._res.status_int = 404
            return self._res

        if hasattr(res, '__class__') and issubclass(res.__class__, Response):
            return res
        if isinstance(res, str) or not res:
            self._res.body = res or ''
        elif isinstance(res, unicode):
            self._res.text = res
        else:
            self._res.app_iter = res

        # return response
        return self._res

    def get_action(self):
        app = os.path.split(os.environ['APPPATH'].rstrip(os.path.sep))[1]
        name = '.'.join([app, 'modules', self._router.module(), 'controllers', self._router.controller()])

        try:
            module = None
            action = self._router.action()
            controller = self._router.controller()

            if name not in sys.modules:
                module = __import__("app.modules.home.controllers.index", fromlist=["index"])
            else:
                module = sys.modules[name]
            return getattr(module, action)

        except (AttributeError, ImportError) as ex:
            print(str(ex))
            return None
