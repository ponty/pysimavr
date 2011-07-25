from proxy import Proxy
from pysimavr.swig.spk import spk_reset, spk_t, spk_core_init, spk_read, \
    spk_buffer_ready
from swig.simavr import get_irq_at
import time


class Spk(Proxy):
    _reserved = 'speed rate read getirq'.split()
    def __init__(self, avr, rate=11025, speed=1.0):
        self.rate = rate
        self.speed = speed
        self.backend = spk_t()
        spk_core_init(avr.backend, self.backend, rate, speed)
    
    def getirq(self, pin):
        return get_irq_at(self.backend.irq , 0)

    def read(self):
#        assert not self.backend.overrun
        i=0
        while not spk_buffer_ready(self.backend):
            i+=1
            time.sleep(0.005)
            if i>1000:
                print '----------'
                break
        buffer = spk_read(self.backend)
#        print 'buffer ', len(buffer), buffer
        spk_reset(self.backend)
#        print 'reseet ', self.backend.start_cycle
        return buffer
