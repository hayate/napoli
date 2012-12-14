#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import inspect
import settings
from configs.routes import routes


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
    def __init__(self):
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
        self._packages = settings.packages
        self._default_package = settings.default['module']
        self._default_controller = settings.default['controller']
        self._default_action = settings.default['action']
        self._package = None
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
            self._package = self._default_package
            self._controller = self._default_controller
            self._action = self._default_action
        else:
            if self._ispackage(segs[0]):
                self._package = segs[0]
                segs.pop(0)
                if not len(segs):
                    self._controller = self._default_controller
                    self._action = self._default_action
                else:
                    if self._ismodule(self._package, segs[0]):
                        self._controller = segs[0]
                        segs.pop(0)
                    else:
                        self._controller = self._default_controller
                    if len(segs) and self._isaction(self._package, self._controller, segs[0]):
                        self._action = segs[0]
                        segs.pop(0)
                    else:
                        self._action = self._default_action
                    if len(segs): self._args = segs
            elif self._ispackage(self._default_package):
                self._package = self._default_package
                if self._ismodule(self._package, segs[0]):
                    self._controller = segs[0]
                    segs.pop(0)
                else:
                    self._controller = self._default_controller
                if len(segs) and self._isaction(self._package, self._controller, segs[0]):
                    self._action = segs[0]
                    segs.pop(0)
                else:
                    self._action = self._default_action
                if len(segs): self._args = segs
            else:
                self._package = self._default_package
                self._controller = self._default_controller
                if self._isaction(self._package, self._controller, segs[0]):
                    self._action = segs[0]
                    segs.pop(0)
                else:
                    self._action = self._default_action
                if len(segs): self._args = segs


    def package(self):
        return self._package

    def controller(self):
        return self._controller

    def action(self):
        return self._action

    def args(self):
        return self._args

    def _ispackage(self, package):
        if package == 'common':
            return os.path.isdir(os.path.join(self._basepath, package, 'controllers'))
        path = os.path.join(self._basepath, 'packages', package, 'controllers')
        return package in self._packages and os.path.isdir(path)

    def _ismodule(self, package, name):
        if package == 'common':
            return os.path.isfile(os.path.join(self._basepath, package, 'controllers', '.'.join([name, 'py'])))
        filepath = os.path.join(self._basepath, 'packages', package, 'controllers', '.'.join([name, 'py']))
        return os.path.isfile(filepath)

    def _isaction(self, package_name, module_name, action_name):
        if action_name.startswith('_'): return False

        if package_name == 'common':
            module = '.'.join(['application', package_name, 'controllers', module_name])
        else:
            module = '.'.join(['application','packages',package_name,'controllers',module_name])
        try:
            class_name = ''.join([s.lower().capitalize() for s in module_name.split('_')])
            klass = __import__(module, fromlist=[class_name])
            for name, obj in inspect.getmembers(klass, inspect.isclass):
                if name == class_name:
                    return action_name in dir(obj)

            return False
        except ImportError:
            return False

    def __str__(self):
        return 'package: %s - controller: %s - action: %s' % (self._package, self._controller, self._action)