from proxy import Proxy
from swig.ledrow import ledrow_t,ledrow_core_init
from swig.simavr import get_irq_at


class LedRow(Proxy):
    _reserved = 'getirq pinstate reset_dirty'.split()
    def __init__(self, avr, size=8):
        self.backend = ledrow_t()
        ledrow_core_init(avr.backend, self.backend, size)
    
    def _getirq(self, index):
        return get_irq_at(self.backend.irq , index)
    
    def getirq(self, pin):
        return self._getirq(int(pin))

    def pinstate(self, i):
        return bool(self.backend.pinstate & (1<<i))
    
    def reset_dirty(self, i):
        'read and reset'
        x= bool(self.backend.pinstate_changed & (1<<i))
        self.backend.pinstate_changed &=~(1<<i)
        return x
