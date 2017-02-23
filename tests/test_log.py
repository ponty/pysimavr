from nose.tools import eq_
from pysimavr.swig.simavr import avr_make_mcu_by_name, use_mem_logger, \
    mem_logger_read_line, avr_terminate


def test_swig():
    eq_(mem_logger_read_line(), None)
    avr = avr_make_mcu_by_name('atmega48')
    eq_(mem_logger_read_line(), None)
    avr_terminate(avr)
    eq_(mem_logger_read_line(), None)

    use_mem_logger()

    eq_(mem_logger_read_line(), None)
    avr = avr_make_mcu_by_name('atmega48')
    eq_(mem_logger_read_line(),
        'Starting atmega48 - flashend 0fff ramend 02ff e2end 00ff\n')
    eq_(mem_logger_read_line(), None)
    eq_(mem_logger_read_line(), None)
    avr_terminate(avr)
    eq_(mem_logger_read_line(), None)
