from nose.tools import eq_
from pyavrutils import AvrGcc
from pysimavr.avr import Avr
from pysimavr.firmware import Firmware

mcu = 'atmega48'


def test_fw_1():
    cc = AvrGcc(mcu=mcu)
    cc.build('int main(){}')
    fw = Firmware(cc.output)

    avr = Avr(mcu=mcu, firmware=fw, f_cpu=8000000)
    eq_(avr.f_cpu, 8000000)
    eq_(avr.mcu, 'atmega48')


def test_fw_3():
    cc = AvrGcc(mcu=mcu)
    cc.build('int main(){}')
    fw = Firmware(cc.output)

    avr = Avr(mcu=mcu, f_cpu=8000000)
    avr.load_firmware(fw)
    eq_(avr.f_cpu, 8000000)
    eq_(avr.mcu, 'atmega48')
