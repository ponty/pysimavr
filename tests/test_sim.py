from nose.tools import eq_
from pysimavr.avr import Avr
from pysimavr.serial import ArduinoSimSerial

def check_sim(code_snippet, mcu, value):
    eq_(ArduinoSimSerial(snippet=code_snippet, mcu=mcu).serial(), value)
        

def check(mcu):
    check_sim('Serial.print("hi");', mcu, 'hi')
    check_sim('Serial.print(123);', mcu, '123')
    check_sim('delay(1);Serial.print("ok");', mcu, 'ok')

for mcu in Avr.arduino_targets:
    exec '''
def test_{mcu}():
    check("{mcu}")
'''.format(mcu=mcu)