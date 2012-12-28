# server details, port number will increase depending on numer of processes
server = {
    'hostname': 'localhost',
    'port': 10000
}

# process details
process = {
    # number of required process or "max" which means as many process as
    # available cores.
    # if the number of process is creater then available cores then "max"
    # is assumed.
    'number': 1,
    # process will run as
    'user': 'andrea',
    'group': 'nogroup',
    # pidfile path
    'pidpath': '/tmp/',
}

# path to application directory
import os
application = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), 'app')

# levels: DEBUG,INFO,WARNING,ERROR,CRITICAL
logging = {
    'level': 'DEBUG',
    'log_path': os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), 'logs')
}

stdstr = {
    # possible values 'tty' or 'null'
    # 'tty' = send output to terminal
    # 'null' = discard all output
    'stdout': 'tty',
    'stderr': 'tty'
}

# default route
default = {
    'bundle': 'home',
    'controller': 'index',
    'action': 'index',
}

# installed modules
bundles = ('home')
