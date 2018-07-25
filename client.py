#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from client import __version__


def parse_args():
    '''
    Takes command line arguments and parses them to return a valid list.
    If an error ocurs, the program exits.
    '''
    parser = argparse.ArgumentParser(
        description='Arithmetic Calculator Client')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='verbose (debug) log')
    group.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='silent mode, only log warnings and errors')
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument(
        'input_file',
        type=argparse.FileType(),
        help='file with arithmetical operations')
    parser.add_argument(
        'output_file',
        type=argparse.FileType(mode='w'),
        help='file where to store the results')
    args = parser.parse_args()
    return args


def main(args):
    '''Main function that initiates the client itself.'''
    print('Client is running...')


if __name__ == '__main__':
    args = parse_args()
    main(args)
