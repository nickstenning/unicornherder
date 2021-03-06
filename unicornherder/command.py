from __future__ import print_function

import argparse
import logging
import os
import sys

from . import __version__
from .herder import Herder


parser = argparse.ArgumentParser(description='Manage daemonized (g)unicorns.')

parser.add_argument('-u', '--unicorn', default='gunicorn', metavar='TYPE',
                    choices=['unicorn', 'gunicorn'],
                    help='The type of unicorn to manage (gunicorn, unicorn)')
parser.add_argument('-p', '--pidfile', metavar='PATH',
                    help='Path to the pidfile that unicorn will write')
parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument('args', nargs=argparse.REMAINDER,
                    help='Any additional arguments will be passed to unicorn/'
                         "gunicorn. Prefix with '--' if you are passing flags (e.g. "
                         'unicornherder -- -w 4 myapp:app)')


def configure_logger():
    format = '%(asctime)-15s  %(levelname)-8s  %(message)s'
    logging.basicConfig(format=format, level=logging.INFO)

    log = logging.getLogger('unicornherder')

    level = os.environ.get('UNICORNHERDER_LOGLEVEL', '').upper()
    valid_levels = ['CRITICAL', 'FATAL', 'ERROR', 'WARN',
                    'WARNING', 'INFO', 'DEBUG']

    if level in valid_levels:
        log.setLevel(getattr(logging, level))


def main():
    configure_logger()

    args = parser.parse_args()

    if len(args.args) > 0 and args.args[0] == '--':
        args.args.pop(0)

    args.args = ' '.join(args.args)

    if args.pidfile is None:
        args.pidfile = '%s.pid' % args.unicorn

    herder = Herder(**vars(args))
    if herder.spawn():
        return herder.loop()

if __name__ == '__main__':
    sys.exit(main())
