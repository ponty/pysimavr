from nose.tools import eq_
from path import Path
from pysimavr.avr import Avr
from pysimavr.sim import ArduinoSim


def check_sim(snippet, mcu, value, timespan=1):
    eq_(ArduinoSim(
        snippet=snippet, mcu=mcu, timespan=timespan).get_serial(), value)


def check(mcu):
    check_sim('Serial.print("hi");', mcu, 'hi')
    check_sim('Serial.print(123);', mcu, '123')
    check_sim('delay(100);Serial.print("ok");', mcu, 'ok', timespan=0.200)
    check_sim('delay(200);Serial.print("nok");', mcu, '', timespan=0.150)

# for mcu in ['atmega48']:#Avr.arduino_targets:
#     exec '''
# def test_{mcu}():
#     check("{mcu}")
# '''.format(mcu=mcu)
def test_atmega48():
    check("atmega48")


def check_fcpu(f):
    snippet = '''Serial.print(F_CPU);'''
    s = ArduinoSim(
        snippet=snippet,
        f_cpu=f,
        timespan=1).get_serial()
    eq_(int(s), f)


def test_fcpu():
    check_fcpu(20000000)
    check_fcpu(12000000)
    check_fcpu(16000000)
    check_fcpu(8000000)
    check_fcpu(4000000)
    check_fcpu(1000000)

mcu_h = Path(__file__).parent / 'mcu.h'


def check_mcu(mcu1, mcu2):
    snippet = mcu_h.text() + '''
    Serial.print(MCU_DEFINED);
    '''
    s = ArduinoSim(
        snippet=snippet,
        mcu=mcu1,
        timespan=1).get_serial()
    eq_(s, mcu2)


def test_mcu():
    check_mcu('atmega48', '__AVR_ATmega48__')
#     check_mcu('atmega88', '__AVR_ATmega88__')
#     check_mcu('atmega168', '__AVR_ATmega168__')
#     check_mcu('atmega328p', '__AVR_ATmega328P__')
#     check_mcu('atmega8', '__AVR_ATmega8__')
