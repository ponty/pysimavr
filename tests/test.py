from nose.tools import eq_, timed
from pysimavr.ac import Ac
from pysimavr.avr import Avr
from pysimavr.lcd import Lcd
from pysimavr import sgm7
from pysimavr import ledrow
from pysimavr import inverter

def test_avr():
    avr = Avr(mcu='atmega48', f_cpu=8000000)

    eq_(avr.f_cpu, 8000000)
    eq_(avr.mcu, 'atmega48')
    eq_(avr.pc, 0)
    avr.step(1)
    eq_(avr.pc, 2)
    
# TODO: segfault in alltest
#def test_ac():
#    avr = Avr(mcu='atmega48', f_cpu=8000000)
#    ac = Ac(avr)

