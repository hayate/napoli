#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pwd
import grp
import sys
from gevent import monkey
monkey.patch_all()
from gevent import pywsgi
from lib.daemon import Daemon
from lib.config import Config
from napoli import Napoli



class Worker(Daemon):
    def __init__(self, hostname, port, name):
        """
        hostname (str): The server hostname
        port (int): Port number of the server
        config (object): Config
        """
        self.hostname = hostname
        self.port = port
        self.config = Config(name)
        stdout = '/dev/null'
        stderr = '/dev/null'
        if self.config.stdstr['stdout'] == 'tty':
            stdout = os.popen('tty').read().strip()
        if self.config.stdstr['stderr'] == 'tty':
            stderr = os.popen('tty').read().strip()

        pidfile = os.path.join(self.config.process['pidpath'],
                               "napoli_{0}_{1}.pid".format(hostname, port))
        super(Worker, self).__init__(pidfile, stdout=stdout, stderr=stderr)

    def daemonize(self):
        haspid = os.path.isfile(self.pidfile)
        super(Worker, self).daemonize()

        username = pwd.getpwuid(os.getuid()).pw_name
        if username != self.config.process['user']:
            uid = pwd.getpwnam(self.config.process['user']).pw_uid
            gid = grp.getgrnam(self.config.process['group']).gr_gid
            os.chown(self.pidfile, uid, gid)
            os.setgid(gid)
            os.setuid(uid)

        if not haspid and os.path.isfile(self.pidfile):
            print("Starting daemon with pid: {0}".format(self.pidfile))

    def run(self):
        try:
            server = pywsgi.WSGIServer((self.hostname, self.port), Napoli())
            server.serve_forever()
        except Exception as e:
            print("Could not start server: {0}".format(e))

    def stop(self):
        haspid = os.path.isfile(self.pidfile)
        super(Worker, self).stop()
        if haspid and not os.path.isfile(self.pidfile):
            print("Stopped daemon with pid: {0}".format(self.pidfile))

def usage():
    print("usage: {0} -h hostname -p port -c config start|restart|stop".format(sys.argv[0]))

if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            command = sys.argv.pop()
            hostname = sys.argv[sys.argv.index('-h') + 1]
            port = int(sys.argv[sys.argv.index('-p') + 1])
            name = Config(sys.argv[sys.argv.index('-c') + 1])
            worker = Worker(hostname, port, name)
            if 'start' == command:
                worker.start()
            elif 'stop' == command:
                worker.stop()
            elif 'restart' == command:
                worker.restart()
            else:
                print("{0} is an invalid command.".format(command))
                usage()
        else:
            usage()
    except ValueError:
        usage()

