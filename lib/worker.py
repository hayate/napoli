#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pwd
import grp
from multiprocessing import Process
from gevent import pywsgi
import settings

class Worker(object):
    def __init__(self, hostname, port, app):
        """
        hostname (str): The server hostname
        port (int): Port number of the server
        app (object): The wsgi app
        """
        self.hostname = hostname
        self.port = port
        self.app = app
        self.proc = Process(target=self, name="{0}{1}".format(hostname, port))
        self.proc.daemon = True

    def pid(self):
        return self.proc.pid

    def start(self):
        self.proc.start()

    def stop(self):
        self.proc.terminate()

    def __call__(self):
        server = pywsgi.WSGIServer((self.hostname, self.port), self.app)
        try:
            server.serve_forever()
        except Exception as e:
            print("Could not start server: {0}".format(e))






