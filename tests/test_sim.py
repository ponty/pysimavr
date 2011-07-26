from nose.tools import eq_
from pysimavr.avr import Avr
from pysimavr import sim

def check_sim(code_snippet, mcu, value):
    eq_(sim.code2ser(code_snippet, mcu), value)
        

def check(mcu):
    check_sim('delay(1);Serial.print("ok");', mcu, 'ok')

for mcu in Avr.arduino_targets:
    exec '''
def test_{mcu}():
    check("{mcu}")
'''.format(mcu=mcu)