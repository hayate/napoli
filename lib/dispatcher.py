#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import inspect
from webob import Response
from lib.controller import Controller


class Dispatcher(object):
    def __init__(self, request, router):
        self._req = request
        self._router = router
        self._res = Response()

    def dispatch(self):
        try:
            # if router failed, return 404
            if not self._router.bundle() or not self._router.controller() or not self._router.action():
                return self.not_found()

            # retrieve controller class object, on failure return 404
            cls = self.get_class(self._router.controller(), self._router.bundle())
            if not cls:
                return self.not_found()

            # retrieve controller bound action, on failure return 404
            action = self.get_action(cls, self._router.action())
            if not action:
                return self.not_found()

            # check method number of arguments
            spec = inspect.getargspec(action)
            defc = len(spec.defaults) if spec.defaults else 0
            # required arguments count
            reqc = (len(spec.args) - 1) - defc
            argc = len(self._router.args())
            if not spec.varargs and ((argc < reqc) or (argc > (len(spec.args) - 1))):
                return self.not_found()

            # call controller action
            res = action(*self._router.args())

            # set/return response
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

        except Exception as ex:
            print(ex)


    def not_found(self):
        self._res.status_int = 404
        if self._req.method != 'HEAD':
            self._res.body = 'Not Found'
        return self._res

    def get_action(self, cls, action):
            """
            Return callable controller method or None if action
            is not found in cls

            cls (Controller): controller class object (i.e. not instance)
            action (str): name of controller action
            """
            try:
                if not issubclass(cls, Controller):
                    raise TypeError('Controller must subclass: {0}'.format(Controller.__module__))
                obj = cls()
                obj.request = self._req
                obj.response = self._res
                return getattr(obj, action)

            except AttributeError:
                return None

    def get_class(self, controller, bundle):
        """
        Loads the module containing the controller class
        and returns the controller class object (i.e. not the instance)

        bundle (str): one of the installed bundles
        controller (str): name of the module containing the controller class
        """
        app = os.environ['APPPATH'].strip(os.path.sep).split(os.path.sep).pop()
        name = '.'.join([app,'bundles',bundle,'controllers',controller])

        cls = ''.join([s.lower().capitalize() for s in controller.split('_')])
        try:
            module = None
            if name not in sys.modules:
                module = __import__(name, fromlist=[cls])
            else:
                module = sys.modules[name]
            return getattr(module, cls)

        except (AttributeError, ImportError):
            Log.getInstance().error(traceback.format_exc())
            return None

