#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from server import __version__


def parse_args(raw_args):
    '''
    Takes command line arguments and parses them to return a valid list.
    If an error ocurs, the program exits.
    '''
    parser = argparse.ArgumentParser(
        description='Arithmetic Calculator Server')
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='sets the logging level to DEBUG')
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__))
    args = parser.parse_args(raw_args)
    return args


def main():
    '''
    Main function that initiates the server itself.
    '''
    print('Server is running...')


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    main()
