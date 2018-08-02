import sys
import logging
from multiprocessing import Process, current_process
from server.calculation.shunting_yard import compute


class OperationConsumer(Process):
    '''
    Process derived class.
    Consumes lists of operations in raw strings through its pipe,
    computates results and sends back another list containing them.
    '''

    def __init__(self, pipe):
        Process.__init__(self)
        self._pipe = pipe

    def run(self):
        '''Method that is executed when the process has been started'''
        self._logger = logging.getLogger(
            '{}:{}'.format(__name__, current_process().name))
        try:
            self._running = True
            while self._running:
                if self._pipe.poll():
                    msg = self._pipe.recv()
                    if msg == 'quit':
                        self._running = False
                        self._pipe.close()
                    else:
                        ops = msg
                        results = []
                        for op in ops:
                            try:
                                r = compute(op)
                                results.append(str(r))
                            except SyntaxError:
                                self._logger.warning(
                                    'The operation "{}" cannot be computed, '
                                    'it will be skipped'.format(op))
                        self._pipe.send(results)
        except (SystemExit, KeyboardInterrupt):
            # Exit from process and wait for server to handle situation
            self._running = False
            self._pipe.close()
            sys.exit(1)
