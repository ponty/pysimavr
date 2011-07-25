from proxy import Proxy
from swig.inverter import inverter_t, inverter_core_init, IRQ_INVERTER_IN, \
    IRQ_INVERTER_OUT
from swig.simavr import get_irq_at
import time


class Inverter(Proxy):
    _reserved = 'getirq pinstate'.split()
    _pins=dict(
               IN=IRQ_INVERTER_IN,
               OUT=IRQ_INVERTER_OUT,
               )
    def __init__(self, avr):
        self.backend = inverter_t()
        inverter_core_init(avr.backend, self.backend)
    
    def _getirq(self, index):
        return get_irq_at(self.backend.irq , index)
    
    def getirq(self, pin):
        return self._getirq(self._pins[pin])

    def out(self, i):
        return bool(self.backend.out & (1 << i))
    
