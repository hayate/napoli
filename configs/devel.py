# server details, port number will increase depending on numer of processes
server = {
    'hostname': 'localhost',
    'port': 10000
}

# process details
process = {
    # number of required process or "max" which means as many process as available cores
    # if the number of process is creater then available cores then "max" is assumed
    'number': 'max',
    # process will run as
    'user': 'nobody',
    'group': 'nogroup',
    # pidfile path
    'pidpath': '/tmp/',
}

stdstr = {
    # possible values 'tty' or 'null'
    # 'tty' = send output to terminal
    # 'null' = discard all output
    'stdout': 'tty',
    'stderr': 'tty'
}
