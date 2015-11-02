from pysimavr.proxy import Proxy
from pysimavr.swig.simavr import avr_vcd_t, avr_vcd_start, avr_vcd_stop, avr_vcd_init, \
    avr_vcd_add_signal, avr_vcd_close
import logging

log = logging.getLogger(__name__)


class VcdFile(Proxy):
    _reserved = 'terminate start stop add_signal'.split()

    def __init__(self, avr, filename="gtkwave_output.vcd", period=10):
        '''period : usec

        if period is too high:
        _avr_vcd_notify lcd.D4 overrun value buffer 256
        '''
        self.backend = avr_vcd_t()
        avr_vcd_init(avr.backend, str(filename), self.backend, period)

    def start(self):
        avr_vcd_start(self.backend)

    def stop(self):
        avr_vcd_stop(self.backend)

    def add_signal(self, irq, name=None, bits=1):
        if not name:
            name = irq.name
        log.debug('vcd.add_signal: %s' % name)
        avr_vcd_add_signal(self.backend, irq, bits, name)

    _terminated = False

    def terminate(self):
        if self._terminated:
            return
        self._terminated = True
        log.debug('terminating...')
        avr_vcd_close(self.backend)
        log.debug('...ok')

    def __del__(self):
        self.terminate()
