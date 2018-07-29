import socket
import struct
import logging
from multiprocessing import Process, Pipe
from server.arithmetics.precedence_climbing import compute


class CalculationServer():
    '''
    Server class of the arithmetical calculator.

    This server opens a socket to receive arithmetical operations through it.
    These operations are evaluated to return a result back to the client.
    '''

    def __init__(self, host, port, processes):
        '''Initialize the Server class with the given args.'''
        self.address = (host, port)
        self._processes = processes
        self._logger = logging.getLogger(__name__)
        self.running = False

    def run(self):
        '''Starts running the server on the given address.'''
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
        self._logger.info('Server stopped')

    def send(self, connection, data):
        '''Sends the data.'''
        binary_data = struct.pack('>I', len(data)) + data.encode('utf8')
        self._logger.info('Sending data')
        connection.sendall(binary_data)
        self._logger.debug('Sent data:\n{}'.format(data))
        self._logger.info('Data sent successfully')

    def recv(self, connection):
        '''Receives data.'''
        raw_size = self._recv_all(connection, 4)
        if not raw_size:
            return None
        size = struct.unpack('>I', raw_size)[0]
        recv_data = self._recv_all(connection, size).decode('utf8').rstrip()
        self._logger.debug('Received data:\n{}'.format(recv_data))
        self._logger.info(
            'Received data from {}:{} successfully'
            .format(*connection.getsockname()))
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
        results = []
        self._logger.info('Starting evaluation of operations')

        # pool = []
        # for _ in range(self._processes):
        #     parent_pipe, child_pipe = Pipe()
        #     p = Process(
        #         target=self._evaluate, args=(child_pipe,))
        #     pool.append((p, parent_pipe))
        #     p.start()

        for i, op in enumerate(data.splitlines()):
            try:
                r = compute(op)
            except Exception:
                self._logger.warning(
                    'This operation cannot be processed: {}\n'
                    'Skipping this line'.format(op),
                    exc_info=True)
                continue
            self._logger.debug('Iteration {}: {} = {}'.format(i, op, r))
            
            results.append(str(r))
        self._logger.info('Finished evaluation of operations')
        res = '\n'.join(results)
        self.send(connection, res)
        self._logger.info('Data sent back to client successfully')

    # def _evaluate(self, pipe):
    #     while True:
    #         operation = pipe.recv()
    #         try:
    #             result = compute(operation)
    #             self._logger.debug(
    #                 'Iteration {}: {} = {}'.format(index, operation, result))
    #         except Exception:
    #             self._logger.warning(
    #                 'This operation cannot be processed: "{}"\n'
    #                 'Skipping this line'.format(operation),
    #                 exc_info=True)
