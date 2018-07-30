import logging
from multiprocessing import Process, current_process
from server.calculation.precedence_climbing import compute


class OperationConsumer(Process):

    def __init__(self, pipe):
        Process.__init__(self)
        self._pipe = pipe
        self._running = True

    def run(self):
        self._logger = logging.getLogger(
            '{}:{}'.format(__name__, current_process().name))
        while self._running:
            if self._pipe.poll():
                msg = self._pipe.recv()
                if msg == 'quit':
                    self._running = False
                    self._pipe.close()
                else:
                    order, ops = msg
                    res = []
                    for op in ops:
                        try:
                            r = compute(op)
                            res.append(str(r))
                        except SyntaxError:
                            self._logger.warning(
                                'This operation cannot be processed: "{}"\n'
                                'Skipping this line'.format(op),
                                exc_info=True)
                    self._pipe.send((order, res))
