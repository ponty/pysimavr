from nose.tools import eq_, timed
from pysimavr.avr import Avr

def test_avr():
    avr = Avr(mcu='atmega48', f_cpu=8000000)

    eq_(avr.f_cpu, 8000000)
    eq_(avr.mcu, 'atmega48')
    eq_(avr.pc, 0)
    avr.step(1)
    eq_(avr.pc, 2)
    

