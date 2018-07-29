import socket
import unittest
from threading import Thread
from client import CalculationClient


class ClientTest(unittest.TestCase):
    '''Client TestCase'''

    def run_fake_server(self):
        fake_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fake_server.bind(('', 1000))
        fake_server.listen(0)
        fake_server.accept()
        fake_server.close()

    def test_socket_connected(self):
        '''Test the client socket can connect a server socket'''
        server_thread = Thread(target=self.run_fake_server)
        server_thread.start()

        client = CalculationClient()
        try:
            client.connect('localhost', 1000)
            self.assertTrue(
                client._socket.getpeername() == ('127.0.0.1', 1000))
        finally:
            server_thread.join()
