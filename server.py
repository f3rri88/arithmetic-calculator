#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import time
import argparse
import logging
import logging.config
from pathlib import Path
from threading import Thread
from server import __version__, CalculationServer


logger = logging.getLogger(__name__)


def processes_type(x):
    x = int(x)
    if x < 2:
        raise argparse.ArgumentTypeError("Minimum number of processes is 2")
    return x


def port_type(x):
    x = int(x)
    if x < 0 or x > 65535:
        raise argparse.ArgumentTypeError(
            "Port value must be between 0 and 65535")
    return x


def parse_args():
    '''
    Takes command line arguments and parses them to return a valid list.
    '''
    parser = argparse.ArgumentParser(
        description='Arithmetic Calculator Server')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-v',
        '--verbose',
        action='store_const',
        const=logging.DEBUG,
        dest='logging_level',
        default=logging.INFO,
        help='verbose (debug) log')
    group.add_argument(
        '-q',
        '--quiet',
        action='store_const',
        const=logging.WARN,
        dest='logging_level',
        default=logging.INFO,
        help='silent mode, only log warnings and errors')
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__))
    parser.add_argument(
        '-p',
        '--processes',
        type=processes_type,
        metavar='X',
        default=2,
        help='Number of processes that the server will spawn')
    parser.add_argument(
        '--port',
        type=port_type,
        default=1234,
        help='Port where to run the server on')
    args = parser.parse_args()
    return args


def setup_logging(log_level):
    '''Setup logging configuration'''
    config_file = Path.cwd() / 'server' / 'config' / 'logging.yml'
    if config_file.is_file():
        with open(config_file, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        root = logging.getLogger()
        root.setLevel(log_level)
    else:
        logger.warn(
            'logging.yml file was not found in "server/config/" folder, '
            'using default configuration for logging')
        logging.basicConfig(level=log_level)


def main():
    '''Main function that initiates the server itself.'''
    # Get input arguments
    args = parse_args()

    setup_logging(args.logging_level)

    # Start our server
    server = CalculationServer('0.0.0.0', args.port, args.processes)
    try:
        server.run()
    except:
        sys.exit(1)


if __name__ == '__main__':
    main()
