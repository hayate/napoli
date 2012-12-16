#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import settings


class Route(object):
    def __init__(self, pattern, target):
        self._pattern = re.compile(pattern, re.IGNORECASE)
        self.target = target
        self.pattern = pattern

    def match(self, path):
        match = self._pattern.match(path)
        if match:
            return re.sub(self.pattern, self.target, path)
        return None


class Routes(object):
    def __init__(self, routes):
        self._routes = routes

    def add_route(self, route, target=None):
        if isinstance(route, Route):
            self._routes[route.pattern] = route
        else:
            self._routes[route] = Route(route, target)

    def remove_route(self, route):
        try:
            if isinstance(route, Route):
                self._routes.pop(route.pattern)
            else:
                self._routes.pop(route)
            return True
        except KeyError:
            return False

    def find_match(self, path):
        for route in self._routes.values():
            routed = route.match(path)
            if routed:
                return routed
        return path


class Router(object):
    def __init__(self, routes):
        """
        routes: (Routes)
        """
        self._modules = settings.modules
        self._default_module = settings.default['module']
        self._default_controller = settings.default['controller']
        self._default_action = settings.default['action']
        self._module = None
        self._controller = None
        self._action = None
        self._basepath = os.environ['APPPATH']
        self._routes = routes
        self._args = []

    def route(self, path_info):
        path = self._routes.find_match(path_info)
        segs = []
        for seg in path.strip('/').split('/'):
            seg = seg.strip()
            if len(seg): segs.append(seg)

        if not len(segs):
            self._module = self._default_module
            self._controller = self._default_controller
            self._action = self._default_action
        else:
            if self._ismodule(segs[0]):
                self._module = segs[0]
                segs.pop(0)
                if not len(segs):
                    self._controller = self._default_controller
                    self._action = self._default_action
                else:
                    if self._ismodule(self._module, segs[0]):
                        self._controller = segs[0]
                        segs.pop(0)
                    else:
                        self._controller = self._default_controller
                    if len(segs) and self._isaction(self._module, self._controller, segs[0]):
                        self._action = segs[0]
                        segs.pop(0)
                    else:
                        self._action = self._default_action
                    if len(segs): self._args = segs
            elif self._ismodule(self._default_module):
                self._module = self._default_module
                if self._ismodule(self._module, segs[0]):
                    self._controller = segs[0]
                    segs.pop(0)
                else:
                    self._controller = self._default_controller
                if len(segs) and self._isaction(self._module, self._controller, segs[0]):
                    self._action = segs[0]
                    segs.pop(0)
                else:
                    self._action = self._default_action
                if len(segs): self._args = segs
            else:
                self._module = self._default_module
                self._controller = self._default_controller
                if self._isaction(self._module, self._controller, segs[0]):
                    self._action = segs[0]
                    segs.pop(0)
                else:
                    self._action = self._default_action
                if len(segs): self._args = segs


    def module(self):
        return self._module

    def controller(self):
        return self._controller

    def action(self):
        return self._action

    def args(self):
        return self._args

    def _ismodule(self, module):
        path = os.path.join(self._basepath, 'modules', module, 'controllers')
        return module in self._modules and os.path.isdir(path)

    def _iscontroller(self, module, name):
        filepath = os.path.join(self._basepath, 'modules', module, 'controllers', '.'.join([name, 'py']))
        return os.path.isfile(filepath)

    def _isaction(self, module_name, controller_name, action_name):
        if action_name.startswith('_'): return False

        app = os.path.split(os.environ['APPPATH'].rstrip(os.path.sep))[1]
        module = '.'.join([app, 'modules', module_name, 'controllers', controller_name])
        try:
            controller = __import__(module)
            return action_name in dir(controller)
        except ImportError:
            return False

    def __str__(self):
        return 'module: %s - controller: %s - action: %s' % (self._module, self._controller, self._action)