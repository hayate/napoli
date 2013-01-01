#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import functools
import sys


class Plugin(object):
    def __init__(self, name=None):
        self.name = name
        self.active = False

    def run(self, callback):
        raise NotImplementedError

    def __call__(self, callback):
        return self.run(callback)

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

    def uninstall(self, name):
        try:
            del self.__plugins[name]
        except KeyError:
            pass

    def install(self, name, *a, **kw):
        if name in self.__plugins:
            return
        plugin = self.load(name, *a, **kw)
        if plugin:
            plugin.active = True
            self.__plugins[name] = plugin

    def load(self, name, *a, **kw):
        if name in self.__plugins:
            return self.__plugins[name]

        name = name.lower()
        klass = ''.join([name.capitalize(), 'Plugin'])
        mod = '.'.join(['plugins', klass.lower()])
        module = None
        if mod not in sys.modules:
            module = __import__(mod, fromlist=[klass])
        else:
            module = sys.modules[mod]

        klass = getattr(module, klass)
        if issubclass(klass, Plugin):
            obj = klass()
            obj.setup(*a, **kw)
            return obj
        raise TypeError('%s is not a sub-class of %s' % (klass, Plugin))


def apply_plugin(*names):
    """
    names (list): the list of plugins to add
    """
    def decorator(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            plugins = Plugins()
            _addplug = getattr(callback, '_addplug', {})
            for name in _addplug:
                if name not in plugins:
                    plugin = plugins.load(name)
                    if plugin:
                        plugin.active = True
                        _addplug[name] = plugin
            setattr(callback, '_addplug', _addplug)
            return callback(*args, **kwargs)
        return wrapper
    return decorator


def skip_plugin(*names):
    """
    names (list): a list of plugins to skip
    """
    def decorator(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            _skipplug = getattr(callback, '_skipplug', [])
            _skipplug = list(set(_skipplug + names))
            setattr(callback, '_skipplug', _skipplug)
            return callback(*args, **kwargs)
        return wrapper
    return decorator
