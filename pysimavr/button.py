from proxy import Proxy
from swig.simavr import get_irq_at

from swig.button import button_press, IRQ_BUTTON_OUT, button_init, button_t, button_down, button_up, button_press
import logging

log = logging.getLogger(__name__)

class Button(Proxy):
    _reserved = 'getirq down up press'.split()
    def __init__(self, avr, pullup=True):
        self.backend = button_t()
        self.name = 'button'
        button_init(avr.backend, self.backend, self.name, pullup)
    
    def _getirq(self, index):
        return get_irq_at(self.backend.irq , index)
    
    def getirq(self, pin):
        return self._getirq(IRQ_BUTTON_OUT)
    
    def down(self):
        log.debug('button_down')
        button_down(self.backend)

    def up(self):
        log.debug('button_up')
        button_up(self.backend)

    def press(self, duration):
        log.debug('button_press')
        button_press(self.backend, duration)



