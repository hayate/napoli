#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from multiprocessing import cpu_count
from subprocess import Popen


if __name__ == "__main__":
    cwd = os.path.dirname(os.path.realpath(__file__))
    try:
        if len(sys.argv) > 1:
            # number of cores
            cores = cpu_count()
            # start|stop|restart|status
            command = sys.argv.pop()
            hostname = sys.argv[sys.argv.index('-h') + 1]
            port = int(sys.argv[sys.argv.index('-p') + 1])
            # config module
            name = sys.argv[sys.argv.index('-c') + 1]
            # number of process to start
            proc_num = 1
            if '-proc' in sys.argv:
                proc_num = int(sys.argv[sys.argv.index('-proc') + 1])

            if proc_num == "max" or proc_num > cores:
                proc_num = cores

            if 'start' == command:
                for p in range(port, (port + proc_num)):
                    Popen(["python {0}/worker.py -h {1} -p {2} -c {3} {4}".format(cwd, hostname, str(p), name, 'start')], shell=True).wait()
            elif 'stop' == command:
                for p in range(port, (port + proc_num)):
                    Popen(["python {0}/worker.py -h {1} -p {2} -c {3} {4}".format(cwd, hostname, str(p), name, 'stop')], shell=True).wait()
            elif 'restart' == command:
                for p in range(port, (port + proc_num)):
                    Popen(["python {0}/worker.py -h {1} -p {2} -c {3} {4}".format(cwd, hostname, str(p), name, 'restart')], shell=True).wait()
            elif 'status' == command:
                for p in range(port, (port + proc_num)):
                    Popen(["python {0}/worker.py -h {1} -p {2} -c {3} {4}".format(cwd, hostname, str(p), name, 'status')], shell=True).wait()
            else:
                print("{0} Unknown command".format(command))
                sys.exit(2)
            sys.exit(0)
        else:
            print("usage: {0} -h hostname -p port [-proc 1~cpu_count()] [-c module] start|stop|restart|status".format(sys.argv[0]))
            sys.exit(2)
    except ValueError:
        print("usage: {0} -h hostname -p port [-proc 1~cpu_count()] [-c module] start|stop|restart|status".format(sys.argv[0]))
        sys.exit(2)

