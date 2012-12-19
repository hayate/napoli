#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pwd
import grp
import sys
from gevent import monkey
from gevent import pywsgi
from lib.daemon import Daemon
from napoli import Napoli
import settings

monkey.patch_all()


class Worker(Daemon):
    def __init__(self, hostname, port):
        """
        hostname (str): The server hostname
        port (int): Port number of the server
        app (object): The wsgi app
        """
        self.hostname = hostname
        self.port = port
        self.app = Napoli()
        stdout = '/dev/null'
        stderr = '/dev/null'
        if settings.stdstr['stdout'] == 'tty':
            stdout = os.popen('tty').read().strip()
        if settings.stdstr['stderr'] == 'tty':
            stderr = os.popen('tty').read().strip()

        pidfile = os.path.join(settings.process['pidpath'],
                               "napoli_{0}_{1}.pid".format(hostname, port))
        super(Worker, self).__init__(pidfile, stdout=stdout, stderr=stderr)

    def daemonize(self):
        haspid = os.path.isfile(self.pidfile)
        super(Worker, self).daemonize()

        username = pwd.getpwuid(os.getuid()).pw_name
        if username != settings.process['user']:
            uid = pwd.getpwnam(settings.process['user']).pw_uid
            gid = grp.getgrnam(settings.process['group']).gr_gid
            os.chown(self.pidfile, uid, gid)
            os.setgid(gid)
            os.setuid(uid)

        if not haspid and os.path.isfile(self.pidfile):
            print("Starting daemon with pid: {0}".format(self.pidfile))

    def run(self):
        try:
            server = pywsgi.WSGIServer((self.hostname, self.port), self.app)
            server.serve_forever()
        except Exception as e:
            print("Could not start server: {0}".format(e))

    def stop(self):
        haspid = os.path.isfile(self.pidfile)
        super(Worker, self).stop()
        if haspid and not os.path.isfile(self.pidfile):
            print("Stopped daemon with pid: {0}".format(self.pidfile))


if __name__ == '__main__':
    if len(sys.argv) == 4:
        hostname = sys.argv[1]
        port = int(sys.argv[2])
        worker = Worker(hostname, port)
        if 'start' == sys.argv[3]:
            worker.start()
        elif 'stop' == sys.argv[3]:
            worker.stop()
        elif 'restart' == sys.argv[3]:
            worker.restart()
        else:
            print("{0} is an invalid command.".format(sys.argv[3]))
    else:
        print("Usage: sudo {0} hostname port [start | stop | restart]".
              format(sys.argv[0]))
