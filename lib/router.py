import os
import re
import sys
import inspect
from configs import routes
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
    def __init__(self):
        self._routes = routes.routes

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
        self._bundles = settings.bundles
        self._default_bundle = settings.default['bundle']
        self._default_controller = settings.default['controller']
        self._default_action = settings.default['action']
        self._bundle = None
        self._controller = None
        self._action = None
        self._basepath = os.environ['APPPATH']
        self._appdir = self._basepath.strip(os.path.sep).split(os.path.sep).pop()
        self._routes = routes
        self._args = []

    def route(self, path_info):
        path = self._routes.find_match(path_info)
        segs = []
        for seg in path.strip('/').split('/'):
            seg = seg.strip()
            if len(seg): segs.append(seg)

        if not len(segs):
            self._bundle = self._default_bundle
            self._controller = self._default_controller
            self._action = self._default_action
        else:
            if self._isbundle(segs[0]):
                self._bundle = segs[0]
                segs.pop(0)
                if not len(segs):
                    self._controller = self._default_controller
                    self._action = self._default_action
                else:
                    if self._iscontroller(self._bundle, segs[0]):
                        self._controller = segs[0]
                        segs.pop(0)
                    else:
                        self._controller = self._default_controller
                    if len(segs) and self._isaction(self._bundle, self._controller, segs[0]):
                        self._action = segs[0]
                        segs.pop(0)
                    else:
                        self._action = self._default_action
                    if len(segs): self._args = segs
            elif self._isbundle(self._default_bundle):
                self._bundle = self._default_bundle
                if self._iscontroller(self._bundle, segs[0]):
                    self._controller = segs[0]
                    segs.pop(0)
                else:
                    self._controller = self._default_controller
                if len(segs) and self._isaction(self._bundle, self._controller, segs[0]):
                    self._action = segs[0]
                    segs.pop(0)
                else:
                    self._action = self._default_action
                if len(segs): self._args = segs
            else:
                self._bundle = self._default_bundle
                self._controller = self._default_controller
                if self._isaction(self._bundle, self._controller, segs[0]):
                    self._action = segs[0]
                    segs.pop(0)
                else:
                    self._action = self._default_action
                if len(segs): self._args = segs


    def bundle(self):
        return self._bundle

    def controller(self):
        return self._controller

    def action(self):
        return self._action

    def args(self):
        return self._args

    def _isbundle(self, bundle):
        path = os.path.join(self._basepath, 'bundles', bundle, 'controllers')
        return bundle in self._bundles and os.path.isdir(path)

    def _iscontroller(self, bundle, name):
        filepath = os.path.join(self._basepath, 'bundles', bundle, 'controllers', '.'.join([name, 'py']))
        return os.path.isfile(filepath)

    def _isaction(self, bundle_name, controller_name, action_name):
        if action_name.startswith('_'): return False

        controller = '.'.join([self._appdir,'bundles',bundle_name,'controllers',controller_name])
        try:
            class_name = ''.join([s.lower().capitalize() for s in controller_name.split('_')])
            klass = __import__(controller, fromlist=[class_name])
            for name, obj in inspect.getmembers(klass, inspect.isclass):
                if name == class_name:
                    return action_name in dir(obj)

            return False
        except ImportError:
            return False

    def __str__(self):
        return 'bundle: %s - controller: %s - action: %s' % (self._bundle, self._controller, self._action)