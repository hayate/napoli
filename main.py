#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from gevent import monkey; monkey.patch_all()
from multiprocessing import cpu_count
from lib.worker import Worker
from lib.server import Server
import settings


def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello World"


if __name__ == "__main__":
    # number of cores
    proc_num = None
    if settings.process['number'] == 'max':
        proc_num = cpu_count()
    elif int(settings.process['number']) > cpu_count():
        proc_num = cpu_count()
    else:
        proc_num = int(settings.process['number'])

    process = []
    port = int(settings.server['port'])
    hostname = settings.server['hostname']

    for i in range(port, (port + proc_num)):
        worker = Worker(hostname, i, application)
        process.append(worker)

    daemon = Server(process)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)


