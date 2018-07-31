import socket
import struct
import logging


class CalculationClient():
    '''
    Client class of the arithmetical calculator.

    This client opens a socket to transmit data to the server and waits
    the for the result.
    '''

    def __init__(self):
        '''Initialize the Client class with the given args.'''
        self._logger = logging.getLogger(__name__)

    def connect(self, host, port):
        '''Connects to a server on the given address.'''
        self._logger.info('Connecting with server on {}:{}'.format(host, port))
        self.server_address = (host, port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._socket.connect((host, port))
        except socket.error:
            self._logger.error(
                'An error has ocurred connecting to the server address',
                exc_info=True)
            self._socket.close()
            raise

        self._logger.info('Connection established')

    def send(self, data):
        '''Sends to the connected endpoint.'''
        if not self._socket:
            self._logger.warn('No connection has been established yet')
            return
        binary_data = struct.pack('>I', len(data)) + data.encode('utf8')
        self._logger.info('Sending data')
        self._socket.sendall(binary_data)
        self._logger.debug('Sent data:\n{}'.format(data))
        self._logger.info('Data sent successfully')

    def recv(self):
        '''Receives data from the connected endpoint.'''
        raw_size = self._recv_all(4)
        if not raw_size:
            return None
        size = struct.unpack('>I', raw_size)[0]
        recv_data = self._recv_all(size).decode('utf8').rstrip()
        self._logger.debug('Received data:\n{}'.format(recv_data))
        self._logger.info(
            'Received data from server successfully')
        return recv_data

    def _recv_all(self, size):
        '''Receives a fixed ammount of data determined by size.'''
        data = b''
        while len(data) < size:
            packet = self._socket.recv(size - len(data))
            if not packet:
                return None
            data += packet
        return data
