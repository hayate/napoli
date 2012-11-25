#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pwd
from gevent import monkey; monkey.patch_all()
from gevent import pywsgi
from multiprocessing import Process
from multiprocessing import cpu_count


def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello World"

def start_server(listener):
    pywsgi.WSGIServer(listener, application).serve_forever()


port = 18000
hostname = 'localhost'
process = []

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            if len(process) > 0:
                for pro in range(len(process)):
                    if pro.is_alive():
                        print('process pid: {0} already runnning'.format(pro.pid))
                    else:
                        pro.daemon = True
                        pro.start()
            else:
                for i in range(cpu_count()):
                    p = Process(target=start_server, args=((hostname, port),))
                    p.daemon = True
                    p.start()
                    print('started server on port: {0}'.format(port))
                    process.append(p)
                    port += 1
        elif 'stop' == sys.argv[1]:
            if len(process) > 0:
                for pro in range(len(process)):
                    if pro.is_alive():
                        print('stopping server pid: {0}'.format(pro.pid))
                        pro.stop()
        elif 'restart' == sys.argv[1]:
            if len(process) > 0:
                for pro in range(len(process)):
                    if pro.is_alive():
                        pro.stop()
                        pro.daemon = True
                        pro.start()
            else:
                for i in range(cpu_count()):
                    p = Process(group='www-data', target=start_server, args=((hostname, port)))
                    p.daemon = True
                    p.start()
                    print('started server on port: {0}'.format(port))
                    process.append(p)
                    port += 1
        else:
            print "Unknown command"
            sys.exit(2)
        print('i should be here')
        # sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)