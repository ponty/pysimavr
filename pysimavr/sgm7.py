from proxy import Proxy
from swig.sgm7 import sgm7_t, sgm7_core_init, sgm7_get_digit_segments, sgm7_reset_dirty
from swig.simavr import get_irq_at


class Sgm7(Proxy):
    _reserved = 'getirq pinstate reset_dirty pins pinindex digit_segments'.split()
    def __init__(self, avr, size=4):
        self.pins = 'A B C D E F G P'.split() + ['D' + str(x) for x in range(size)]
        self.backend = sgm7_t()
        sgm7_core_init(avr.backend, self.backend, size)
    
    def _getirq(self, index):
        return get_irq_at(self.backend.irq , index)
    
    def pinindex(self, pin_name):
        return self.pins.index(pin_name)
    
    def getirq(self, pin):
        return self._getirq(self.pinindex(pin))

    def pinstate(self, pin):
        return bool(self.backend.pinstate & (1 << self.pinindex(pin)))
    
    def digit_segments(self, digit_index):
        return sgm7_get_digit_segments(self.backend, digit_index)
    
    def reset_dirty(self, digit_index):
        'read and reset'
        return sgm7_reset_dirty(self.backend, digit_index)
