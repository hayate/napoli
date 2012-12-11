#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson
import sys
import os
from lib.daemon import Daemon
import settings

class Server(Daemon):
    def __init__(self, workers):
        """
        """
        self.workers = workers

        if settings.stdstr['stdout'] == 'tty':
            stdout = os.popen('tty').read().strip()
        else:
            stdout = '/dev/null'

        if settings.stdstr['stderr'] == 'tty':
            stderr = os.popen('tty').read().strip()
        else:
            stderr = '/dev/null'

        pidfile = os.path.join(settings.process['pidpath'], settings.process['pidfile'])
        super(Server, self).__init__(pidfile=pidfile, stdout=stdout, stderr=stderr)


    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as f:
                pid = simplejson.load(f)
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(int(pid['server']), SIGTERM)
                for p in pid['workers']:
                    os.kill(int(p), SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)


    def run(self):
        try:
            with open(self.pidfile, 'r') as f:
                pid = int(f.read().strip())
        except IOError as e:
            print(e)
            return

        pids = []
        for worker in self.workers:
            worker.start()
            pids.append(worker.pid)

        des = {'server': pid, 'workers': pids}
        with open(self.pidfile, 'w') as f:
            simplejson.dump(des, f)

        uid = pwd.getpwnam(settings.process['user']).pw_uid
        gid = grp.getgrnam(settings.process['group']).gr_gid
        os.chown(self.pidfile, uid, gid)
        os.setgid(gid)
        os.setuid(uid)
