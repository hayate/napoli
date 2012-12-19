#!/usr/bin/env python
# -*- coding: utf-8 -*-

import napoli

print(dir(napoli))


def index(request):
    print request.GET
    return __file__
