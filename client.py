#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import yaml
import argparse
import logging
import logging.config
from pathlib import Path
from socket import error as socket_error
from client import __version__, CalculationClient


logger = logging.getLogger(__name__)


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
        description='Arithmetic Calculator Client')
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
        '--host',
        type=str,
        default='localhost',
        help='Host where the server is running on (default localhost)')
    parser.add_argument(
        '--port',
        type=port_type,
        default=1234,
        help='Port where the server is running on (default 1234)')
    parser.add_argument(
        'input_file',
        type=argparse.FileType(mode='r'),
        help='file with arithmetical operations')
    parser.add_argument(
        'output_file',
        type=argparse.FileType(mode='w'),
        help='file where to store the results')
    args = parser.parse_args()
    return args


def setup_logging(log_level):
    '''Setup logging configuration'''
    config_file = Path.cwd() / 'client' / 'config' / 'logging.yml'
    if config_file.is_file():
        with open(config_file, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        root = logging.getLogger()
        root.setLevel(log_level)
    else:
        logging.basicConfig(level=log_level)


def main():
    '''Main function that initiates the client itself.'''
    # Get input arguments
    args = parse_args()

    setup_logging(args.logging_level)

    # Start our client
    client = CalculationClient()
    try:
        client.connect(args.host, args.port)
    except socket_error:
        logger.error("The connection could not be established", exc_info=True)
        sys.exit(1)

    client.send(args.input_file.read())
    args.input_file.close()

    try:
        data = client.recv()
    except socket_error:
        logger.error(
            "The server connection closed unexpectedly",
            exc_info=True)
        sys.exit(1)
    args.output_file.writelines(data)
    args.output_file.close()


if __name__ == '__main__':
    main()
