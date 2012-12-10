#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pwd
from gevent import monkey; monkey.patch_all()
from multiprocessing import cpu_count


def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello World"


if __name__ == "__main__":
