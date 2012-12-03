from nose.tools import eq_
from pysimavr.avr import Avr
from pysimavr.sim import ArduinoSim


def check_sim(snippet, mcu, value, timespan=0.01):
    eq_(ArduinoSim(
        snippet=snippet, mcu=mcu, timespan=timespan).get_serial(), value)


def check(mcu):
    check_sim('Serial.print("hi");', mcu, 'hi')
    check_sim('Serial.print(123);', mcu, '123')
    check_sim('delay(100);Serial.print("ok");', mcu, 'ok', timespan=0.150)
    check_sim('delay(200);Serial.print("nok");', mcu, '', timespan=0.150)

for mcu in Avr.arduino_targets:
    exec '''
def test_{mcu}():
    check("{mcu}")
'''.format(mcu=mcu)
