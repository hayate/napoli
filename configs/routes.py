#!/usr/bin/env python
# -*- coding: utf-8 -*-

# routes, it uses raw regex to map requests patterns to internal actual valid routes
# routes = {r'^/home/(\d+)/([a-z]+)/(\d+)/?$': r'/home/date/\1/\2/\3'}
# the above is: if we get a request that has: /home/21/May/2012 map it to: /home/date/21/May/2012
routes = {}