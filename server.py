#!/usr/bin/python3

import sys
import argparse
from server import __version__


def parse_args(raw_args):
    parser = argparse.ArgumentParser(description='Arithmetic Calculator Server')
    parser.add_argument("-v", "--version", action='version', version='%(prog)s {version}'.format(version=__version__))
    args = parser.parse_args(raw_args)
    return args


def main():
    print('Server is running...')


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    main()