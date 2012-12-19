#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import functools


class Plugin(object):
    def __init__(self, name=None):
        self.name = name
        self.active = False

    def run(self):
        except NotImplementedError

    def __call__(self):
        self.run()

    def setup(self, *a, **kw):
        pass


class Plugins(object):
    # static
    __plugins = {}

    def __iter__(self):
        return self.__plugins.__iter__()

    def __len__(self):
        return len(self.__plugins)

    def __contains__(self, name):
        return name in self.__plugins

    def __getitem__(self, name):
        return self.__plugins[name]

    def activate(self, name):
        if name in self.__plugins:
            self.__plugins[name].active = True

    def deactivate(self, name):
        if name in self.__plugins:
            self.__plugins[name].active = False

    def install(self, name, *a, **kw):
        if name in self.__plugins:
            return
        plugin = self.load(name)
        if plugin:
            plugin.active = True
            self.__plugins[name] = plugin

    def uninstall(self, name):
        try:
            del self.__plugins[name]
        except KeyError:
            pass

    def load(self, name, *a, **kw):
        if name in self.__plugins:
            return self.__plugins[name]

        name = name.lower()
        klass = ''.join([name.capitalize(), 'Plugin'])
        app = os.path.split(os.environ['APPPATH'].rstrip(os.path.sep))[1]
        mod = '.'.join([app, 'plugins', klass.lower()])
        module = None
        if mod not in sys.modules:
            module = __import__(mod, fromlist=[klass])
        else:
            module = sys.modules[mod]

        klass = getattr(module, klass)
        obj = klass(name)
        if issubclass(klass, Plugin):
            obj.setup(*a, **kw)
            return obj
        raise TypeError('%s is not a sub-class of %s' % (klass, Plugin))

'''
import functools

def suppress_errors(log_func=None):

    """Automatically silence any errors that occur within a function"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)

            except Exception as e:

                if log_func is not None:
                    log_func(str(e))

        return wrapper

return decorator
'''


def apply_plugin(*names):
    """ The plugin decorator

    names (list): a list of plugins name

    """
    def decorator(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            plugins = Plugins()
            for name in names:
                # will do nothing if plugin is already installed
                plugins.install(name)
            for plugin in plugins:
                callback = plugin(callback)
            return callback(*args, **kwargs)
        return wrapper
    return decorator
