from pysimavr.swig.simavr import use_mem_logger, mem_logger_read_line, mem_logger_last_log_level
from threading import Thread
import logging
import time


log = logging.getLogger(__name__)





class SimavrLogger(object):

    _level_map = [
         logging.FATAL, #LOG_OUTPUT = 0,
         logging.ERROR, #LOG_ERROR, 
         logging.WARNING,#LOG_WARNING,
         logging.DEBUG #LOG_TRACE,       
        ]
    
    def __init__(self):
        '''
        '''
        use_mem_logger()
        t = Thread(target=self._log_reader)
        t.name = "Logger"
        t.daemon = True
        t.start()

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

    def log(self, line, avr_log_level=-1):
        if avr_log_level < 0: avr_log_level = mem_logger_last_log_level();        
        if avr_log_level < 0 or avr_log_level >= len(SimavrLogger._level_map): 
            avr_log_level =  len(SimavrLogger._level_map);#Debug for unknown
        py_log_level = SimavrLogger._level_map[avr_log_level]
        if not log.isEnabledFor(py_log_level): return;        
        log.log(py_log_level, line.strip());


_simavr_logger = None


def init_simavr_logger():
    global _simavr_logger
    if not _simavr_logger:
        _simavr_logger = SimavrLogger()


def terminate_simavr_logger():
    global _simavr_logger
    if _simavr_logger:
        _simavr_logger.terminate()


