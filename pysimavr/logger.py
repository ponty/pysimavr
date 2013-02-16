from pysimavr.swig.simavr import use_mem_logger, mem_logger_read_line
from threading import Thread
import logging
import time


log = logging.getLogger(__name__)


class SimavrLogger(object):
    def __init__(self):
        '''
        '''
        use_mem_logger()
        Thread(target=self._log_reader).start()

    def __del__(self):
        self.terminate()

    def terminate(self):
        self._terminate_log_thread = True

    _terminate_log_thread = False

    def _log_reader(self):
        while not self._terminate_log_thread:
            s = mem_logger_read_line()
            if s:
                self.log(s)
            else:
                time.sleep(0.01)

    def log(self, line):
        log.debug(line)


_simavr_logger = None


def init_simavr_logger():
    global _simavr_logger
    if not _simavr_logger:
        _simavr_logger = SimavrLogger()


def terminate_simavr_logger():
    global _simavr_logger
    if _simavr_logger:
        _simavr_logger.terminate()
