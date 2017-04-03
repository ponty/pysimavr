from nose.tools import eq_
from pyavrutils import AvrGcc
from pysimavr.avr import Avr
from pysimavr.firmware import Firmware
from pysimavr.swig.simavr import cpu_Running 
from time import sleep

mcu = 'atmega48'


def test_fw_1():
    cc = AvrGcc(mcu=mcu)
    cc.build('int main(){}')
    fw = Firmware(cc.output)

    avr = Avr(mcu=mcu, firmware=fw, f_cpu=8000000)
    eq_(avr.f_cpu, 8000000)
    eq_(avr.frequency, avr.f_cpu)
    eq_(avr.mcu, 'atmega48')
    avr.terminate()


def test_fw_3():
    cc = AvrGcc(mcu=mcu)
    cc.build('int main(){}')
    fw = Firmware(cc.output)

    avr = Avr(mcu=mcu, f_cpu=8000000)
    avr.load_firmware(fw)
    eq_(avr.f_cpu, 8000000)
    eq_(avr.frequency, avr.f_cpu)
    eq_(avr.mcu, 'atmega48')
    avr.terminate()

def test_background_thread():
    cc = AvrGcc(mcu=mcu)
    cc.build('int main(){}')
    fw = Firmware(cc.output)
    avr = Avr(mcu=mcu, firmware=fw, f_cpu=8000000)    
    eq_(avr.state, cpu_Running, "mcu is not running")
    avr.goto_cycle(100)
    eq_(avr.state, cpu_Running, "mcu is not running")
    avr.terminate()
