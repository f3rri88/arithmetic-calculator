import socket
import struct
import logging
import time
from collections import namedtuple
from multiprocessing import Process, Pipe
from server.calculation import OperationConsumer


ProcessPipe = namedtuple('ProcessPipe', 'process pipe')


class CalculationServer():
    '''
    Server class of the arithmetical calculator.

    This server opens a socket to receive arithmetical operations through it.
    These operations are evaluated to return a result back to the client.
    '''

    def __init__(self, host, port, processes):
        '''Initialize the Server class with the given args.'''
        self.address = (host, port)
        self._process_num = processes
        self._logger = logging.getLogger(__name__)
        self.running = False
        self._process_pool = []

    def run(self):
        '''Starts running the server on the given address.'''
        # Create and bind socket
        self._logger.info(
            'Starting server on {} port {}'.format(*self.address))
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._socket.bind(self.address)
        except socket.error:
            self._logger.error(
                'Error binding to port {}.\n'
                'Maybe is this port already in use?'.format(self.address[1]),
                exc_info=True)
            self._socket.close()
            raise
        self._logger.info('Server is running...')

        # Start listening for requests
        self._socket.listen(1)
        self.running = True
        try:
            while self.running:
                try:
                    connection, address = self._socket.accept()
                    self._logger.info(
                        'Accepted connection from {}:{}'.format(*address))

                    recv_data = self.recv(connection)
                    self._handle_request(connection, recv_data)
                except (SystemExit, KeyboardInterrupt):
                    self._logger.warning(
                        'Keyboard interrupt detected, exiting gracefully')
                    self._socket.shutdown(socket.SHUT_RDWR)
                    self.stop()
                    break
                except Exception:
                    self._logger.critical(
                        'Fatal error', exc_info=True)
                    self.stop()
                    raise

        except (SystemExit, KeyboardInterrupt):
            self._logger.warning('Force exiting...')
            self.stop()
            raise

    def stop(self):
        '''Stops the server.'''
        self._logger.info('Stopping...')
        self.running = False
        self._socket.close()
        if self._process_pool:
            for p in self._process_pool:
                p.process.terminate()
                p.pipe.close()
            self._process_pool.clear()
        self._logger.info('Server stopped')

    def send(self, connection, data):
        '''Sends data to an accepted connection.'''
        binary_data = struct.pack('>I', len(data)) + data.encode('utf8')
        self._logger.info('Sending data')
        connection.sendall(binary_data)
        self._logger.debug('Sent data:\n{}'.format(data))
        self._logger.info('Data sent successfully')

    def recv(self, connection):
        '''Receives data from an accepted connection.'''
        raw_size = self._recv_all(connection, 4)
        if not raw_size:
            return None
        size = struct.unpack('>I', raw_size)[0]
        recv_data = self._recv_all(connection, size).decode('utf8').rstrip()
        self._logger.debug('Received data:\n{}'.format(recv_data))
        self._logger.info(
            'Received data from {}:{} successfully'
            .format(*connection.getpeername()))
        return recv_data

    def _recv_all(self, connection, size):
        '''Receives a fixed ammount of data determined by size.'''
        data = b''
        while len(data) < size:
            packet = connection.recv(size - len(data))
            if not packet:
                return None
            data += packet
        return data

    def _handle_request(self, connection, data):
        '''Handles an accepted connection and sends results back'''
        self._logger.info('Starting computing operations')

        before = time.time()

        def chunks(l, n):
            '''Yield n successive chunks from l.'''
            newn = int(1.0 * len(l) / n + 0.5)
            for i in range(0, n-1):
                yield l[i*newn:i*newn+newn]
            yield l[n*newn-newn:]

        # Create the defined number of processes and
        # send to each one a chunk of data to process
        chunk_gen = chunks(data.splitlines(), self._process_num)
        for _ in range(self._process_num):
            parent_pipe, child_pipe = Pipe(duplex=True)
            p = OperationConsumer(child_pipe)
            self._process_pool.append(ProcessPipe(p, parent_pipe))
            p.start()
            chunk = next(chunk_gen)
            parent_pipe.send(chunk)

        # Iterate through the existing processes to get back the results
        # and wait to the process to join and close pipes
        results = []
        for p in self._process_pool:
            msg = p.pipe.recv()
            p.pipe.send('quit')
            p.process.join()
            p.pipe.close()
            results += msg

        self._process_pool.clear()
        after = time.time()
        self._logger.info('Time taken: {}'.format(after - before))

        self._logger.info('Finished computing operations')
        res = '\n'.join(results)
        self.send(connection, res)
