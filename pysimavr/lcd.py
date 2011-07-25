from proxy import Proxy
from swig.hd44780 import IRQ_HD44780_D0, IRQ_HD44780_D1, IRQ_HD44780_D2, \
    IRQ_HD44780_D3, IRQ_HD44780_D4, IRQ_HD44780_D5, IRQ_HD44780_D6, IRQ_HD44780_D7, \
    IRQ_HD44780_RS, IRQ_HD44780_RW, IRQ_HD44780_E, hd44780_t, hd44780_init, \
    hd44780_get_char,hd44780_reset
from swig.simavr import get_irq_at

class Lcd(Proxy):
    _reserved = 'reset getirq pinstate pins get_char'.split()
    _pins = dict(
               D0=IRQ_HD44780_D0,
               D1=IRQ_HD44780_D1,
               D2=IRQ_HD44780_D2,
               D3=IRQ_HD44780_D3,
               D4=IRQ_HD44780_D4,
               D5=IRQ_HD44780_D5,
               D6=IRQ_HD44780_D6,
               D7=IRQ_HD44780_D7,

               RS=IRQ_HD44780_RS,
               RW=IRQ_HD44780_RW,
               E=IRQ_HD44780_E,
               )
    def __init__(self, avr, size=(20, 2)):
        self.backend = hd44780_t()
        hd44780_init(avr.backend, self.backend, size[0], size[1])
        self.pins = sorted(self._pins.keys())
        
    def _getirq(self, index):
        return get_irq_at(self.backend.irq , index)
    
    def getirq(self, pin):
        index = self._pins[pin]
        return self._getirq(index)
    
    def pinstate(self, pin):
        index = self._pins[pin]
        return bool(self.backend.pinstate & index)
    
    def get_char(self, x, y):
        return hd44780_get_char(self.backend, x, y)

    def reset(self):
        hd44780_reset(self.backend)