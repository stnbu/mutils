# -*- mode: python; coding: utf-8 -*-
"""Daemon for updating `PriceSeries`
"""

import os
import sys
import logging

import daemon
import daemon.pidfile

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def daemonize(main):

    if len(sys.argv) == 1:
        print('usage: {} [--daemon] <directory>'.format(os.path.basename(__file__)))
        sys.exit(1)

    # no need to involve argparse for something this simple
    daemon = True
    if '--daemon' in sys.argv:
        script_name, _, dir_path = sys.argv
    else:
        script_name, dir_path = sys.argv
        daemon = False

    dir_path = os.path.abspath(dir_path)

    if daemon:
        # when I'm a daemon, log all exceptions
        def exception_handler(type_, value, tb):
            logger.exception('uncaught exception: {}'.format(str(value)))
            sys.__excepthook__(type_, value, tb)
        sys.excepthook = exception_handler
        
    logger.debug('starting daemon {} using path {}'.format(script_name, dir_path))

    if daemon:
        with daemon.DaemonContext(
                working_directory=dir_path,
                pidfile=daemon.pidfile.PIDLockFile(os.path.join(dir_path, 'pid')),

        ):
            main(dir_path, daemon=True)
    else:
        main(dir_path, daemon=False)
