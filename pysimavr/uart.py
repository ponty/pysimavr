from pysimavr.swig.uart_buff import uart_buff_t, uart_buff_init, \
    uart_buff_connect, uart_buff_terminate, read_fifo, write_fifo
from threading import Thread
import logging
import string
import time

log = logging.getLogger(__name__)


class Uart():
    _terminate_log_thread = False
    char_logger = None
    line_logger = None
    last_line = ''

    def __init__(self, avr):
        self.buffer = []
        self._line_buffer = ''
        self.backend = uart_buff_t()
        uart_buff_init(avr.backend, self.backend)
        Thread(target=self._uart_reader).start()

    def connect(self):
        uart_buff_connect(self.backend, '0')

    def terminate(self):
        uart_buff_terminate(self.backend)
        self._terminate_log_thread = True

    def __del__(self):
        self.terminate()

    def _uart_reader(self):
        while not self._terminate_log_thread:
            x = read_fifo(self.backend.fifo_in)
            if x == -1:
                time.sleep(0.01)
            else:
                self._uart_log(chr(x))

    def _uart_log(self, c):
        self.buffer.append(c)

        if c not in string.printable:
            x = '.'
        else:
            x = c
        self._line_buffer += x

        if c == '\n':
#            log.debug(self._line_buffer)
            if self.line_logger:
                self.line_logger(self._line_buffer)
            self.last_line = self._line_buffer
            self._line_buffer = ''

        if self.char_logger:
            self.char_logger(c)

    def send_string(self, s):
        for c in s:
            x = write_fifo(self.backend.fifo_out, ord(c))
