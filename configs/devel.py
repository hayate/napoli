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
cwd = os.getcwd()
application = os.path.join(cwd, 'app')

# levels: DEBUG,INFO,WARNING,ERROR,CRITICAL
logging = {
    'level': 'DEBUG',
    'log_path': os.path.join(cwd, 'logs')
}

stdstr = {
    # possible values 'tty' or 'null'
    # 'tty' = send output to terminal
    # 'null' = discard all output
    'stdout': 'tty',
    'stderr': 'tty'
}

# plugins installed by default
plugins = {
    'default': ['json']
}

# default route
default = {
    'bundle': 'home',
    'controller': 'index',
    'action': 'index',
}

# installed modules
bundles = ('home')
