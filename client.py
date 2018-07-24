#!/usr/bin/python3

import sys
import socket


def main(url, port, filepath):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((url, port))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])