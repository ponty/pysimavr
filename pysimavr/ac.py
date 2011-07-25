from proxy import Proxy
from swig.simavr import get_irq_at

from swig.ac_input import IRQ_AC_OUT, ac_input_t,ac_input_init

class Ac(Proxy):
    _reserved = 'getirq'.split()
    def __init__(self, avr):
        self.backend = ac_input_t()
        ac_input_init(avr.backend, self.backend)
    
    def _getirq(self, index):
        return get_irq_at(self.backend.irq , index)
    
    def getirq(self, pin):
        return self._getirq(IRQ_AC_OUT)

    
