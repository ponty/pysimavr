from swig.uart_udp import uart_udp_init, uart_udp_connect, uart_udp_t, uart_udp_terminate
import logging

log = logging.getLogger(__name__)

class Udp():
    def __init__(self, avr):
        self.backend = uart_udp_t()
        uart_udp_init(avr.backend, self.backend);
        
    def connect(self):
        uart_udp_connect(self.backend, '0');
        
    def terminate(self):
        uart_udp_terminate(self.backend)
        
    def __del__(self):
        self.terminate()
