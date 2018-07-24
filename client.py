#!/usr/bin/python3

import sys
import argparse
from client import __version__


def parse_args(raw_args):
    parser = argparse.ArgumentParser(description='Arithmetic Calculator Client')
    #parser.add_argument("-l", "--log-level", choice=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"], help="The logging level")
    parser.add_argument("-v", "--version", action='version', version='%(prog)s {version}'.format(version=__version__))
    # parser.add_argument("url", help="Url where the server is located (like http://localhost:1234)")
    # parser.add_argument("input_file", help="A file with arithmetic operations")
    # parser.add_argument("result_file", help="A file to store the results of the operations")
    args = parser.parse_args(raw_args)
    return args


def main():
    print('Client is running...')


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    main()