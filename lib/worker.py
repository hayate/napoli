#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pwd
import grp
from gevent import pywsgi
from daemon import Daemon
import settings

class Worker(Daemon):
    def __init__(self, hostname, port, app):
        """
        hostname (str): The server hostname
        port (int): Port number of the server
        app (object): The wsgi app
        """
        self.hostname = hostname
        self.port = port
        self.app = app
        self.pidfile = os.path.join(settings.pidpath, ''.join(['napoli_', str(port), '.pid']))
        if settings.stdout['stdout'] == 'tty':
            self.stdout = os.popen('tty').read().strip()
        else:
            self.stdout = '/dev/null'

        if settings.stderr['stdout'] == 'tty':
            self.stderr = os.popen('tty').read().strip()
        else:
            self.stderr = '/dev/null'

        super(Worker, self).__init__(pidfile=self.pidfile, stdout=self.stdout, stderr=self.stderr)


    def run(self):
        uid = pwd.getpwnam(settings.process['user']).pw_uid
        gid = grp.getgrnam(settings.process['group']).gr_gid
        os.setgid(gid)
        os.setuid(uid)
        server = pywsgi.WSGIServer((self.hostname, self.port), self.app)
        server.serve_forever()


