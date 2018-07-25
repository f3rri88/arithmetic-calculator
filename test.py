#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from client import Client
from server import Server


class ClientTest(unittest.TestCase):
    '''Client TestCase'''
    def a_test(self):
        pass


class ServerTest(unittest.TestCase):
    '''Server TestCase'''
    def another_test(self):
        pass


class CommonTest(unittest.TestCase):
    '''CommonLib TestCase'''
    def test_arg_validators(self):
        pass


if __name__ == '__main__':
    unittest.main()
