#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from multiprocessing import cpu_count
from subprocess import Popen
import settings


if __name__ == "__main__":
    # number of cores
    proc_num = None
    if settings.process['number'] == 'max':
        proc_num = cpu_count()
    elif int(settings.process['number']) > cpu_count():
        proc_num = cpu_count()
    else:
        proc_num = int(settings.process['number'])

    port = int(settings.server['port'])
    hostname = settings.server['hostname']
    cwd = os.path.dirname(os.path.realpath(__file__))

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            for p in range(port, (port + proc_num)):
                Popen(["python {0}/worker.py {1} {2} {3}".format(cwd, hostname, str(p), 'start')], shell=True).wait()
        elif 'stop' == sys.argv[1]:
            for p in range(port, (port + proc_num)):
                Popen(["python {0}/worker.py {1} {2} {3}".format(cwd, hostname, str(p), 'stop')], shell=True).wait()
        elif 'restart' == sys.argv[1]:
            for p in range(port, (port + proc_num)):
                Popen(["python {0}/worker.py {1} {2} {3}".format(cwd, hostname, str(p), 'restart')], shell=True).wait()
        else:
            print("{0} Unknown command".format(sys.argv[1]))
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)


