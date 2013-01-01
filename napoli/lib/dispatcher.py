#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import inspect
from webob import Response
from plugins import Plugins
from lib.controller import Controller


class Dispatcher(object):
    def __init__(self, request, router):
        self.req = request
        self.router = router
        self.res = Response()
        self.plugins = Plugins()

    def dispatch(self):
        try:
            # if router failed, return 404
            if not self.router.bundle() or not self.router.controller() or not self.router.action():
                return self.not_found()

            # retrieve controller class object, on failure return 404
            cls = self.get_class(self.router.controller(), self.router.bundle())
            if not cls:
                return self.not_found()

            # retrieve controller bound action, on failure return 404
            action = self.get_action(cls, self.router.action())
            if not action:
                return self.not_found()

            # check method number of arguments
            spec = inspect.getargspec(action)
            defc = len(spec.defaults) if spec.defaults else 0
            # required arguments count
            reqc = (len(spec.args) - 1) - defc
            argc = len(self.router.args())
            if not spec.varargs and ((argc < reqc) or (argc > (len(spec.args) - 1))):
                return self.not_found()

            # apply installed and added plugins
            action = self.apply_plugins(action)
            # call controller action
            res = action(*self.router.args())

            # set/return response
            if hasattr(res, '__class__') and issubclass(res.__class__, Response):
                return res
            if isinstance(res, str) or not res:
                self.res.body = res or ''
            elif isinstance(res, unicode):
                self.res.text = res
            else:
                self.res.app_iter = res

            # return response
            return self.res

        except Exception as ex:
            return self.server_error(ex)

    def apply_plugins(self, method):
        """
        method (instancemethod): apply available plugins before dispatching
        """
        # check if we need to skip any plugin
        _skipplug = getattr(method, '_skipplug', [])
        # skip al plugins if True is in the list
        if True in _skipplug:
            return method

        plugins = getattr(method, '_addplug', {})
        if len(plugins) == 0:
            plugins = self.plugins

        for name in plugins:
            if plugins[name].active and name not in _skipplug:
                method = plugins[name](method)
        return method

    def server_error(self, ex = None):
        """
        return a 500 Server Error response
        """
        self.res.status_int = 500
        if self.req.method != 'HEAD':
            if ex:
                self.res.body = str(ex)
            else:
                self.res.body = 'Internal Server Error'
        return self.res

    def not_found(self):
        """
        return a 404 not found response
        """
        self.res.status_int = 404
        if self.req.method != 'HEAD':
            self.res.body = 'Not Found'
        return self.res


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
            obj.request = self.req
            obj.response = self.res
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

