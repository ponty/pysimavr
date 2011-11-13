from pyavrutils.arduino import Arduino
from pysimavr.avr import Avr
from pysimavr.connect import connect_pins_by_rule
from pysimavr.firmware import Firmware
from pysimavr.udp import Udp
from pysimavr.udpreader import UdpReader
from pysimavr.vcdfile import VcdFile
import logging
import time

log = logging.getLogger(__name__)

TEMPLATE = '''
void setup()
{
    Serial.begin(9600);

    snippet;
    
}

void loop()
{
}
'''

class ArduinoSim(object):
    '''arduino code builder and simulator for serial testing'''
    def __init__(self,
                 snippet=None,
                 mcu='atmega328',
                 f_cpu=16000000,
                 extra_lib=None,
                 timespan=0.01,
                 vcd=None,
                 template=None,
                 code=None,
                 ):
        self.cc = Arduino(mcu=mcu, f_cpu=f_cpu, extra_lib=extra_lib)
        if template:
            self.template = template
        else:
            self.template = TEMPLATE
        self.snippet = snippet
        self.code = code
        self.timespan = timespan # 10ms
        self.vcd = vcd
        self.serial = ''
    
    @property
    def mcu(self):
        return self.cc.mcu

    @mcu.setter
    def mcu(self, value):
        self.cc.mcu = value
   
    def build(self):
        code = self.code
        if not code:
            code = self.template.replace('snippet', self.snippet)
        log.debug('code=%s' % code)
        self.cc.build(code)

    def simulate(self):
        elf = self.cc.output
        
        # run
        firmware = Firmware(elf)
        avr = Avr(mcu=self.cc.mcu, f_cpu=self.cc.f_cpu)
        avr.load_firmware(firmware)
        
        udpReader = UdpReader()
        udp = Udp(avr)
        udp.connect()
        udpReader.start()

        simvcd = None
        if self.vcd:
            simvcd = VcdFile(avr, period=1000, filename=self.vcd)
            connect_pins_by_rule('''
                                avr.D0 ==> vcd
                                avr.D1 ==> vcd
                                avr.D2 ==> vcd
                                avr.D3 ==> vcd
                                avr.D4 ==> vcd
                                avr.D5 ==> vcd
                                avr.D6 ==> vcd
                                avr.D7 ==> vcd
        
                                avr.B0 ==> vcd
                                avr.B1 ==> vcd
                                avr.B2 ==> vcd
                                avr.B3 ==> vcd
                                avr.B4 ==> vcd
                                avr.B5 ==> vcd
                                ''',
                                 dict(
                                      avr=avr,
                                     ),
                                 vcd=simvcd,
            )
            simvcd.start()
            
        avr.move_time_marker(self.timespan)
        
        while avr.time_passed() < self.timespan * 0.99:
            time.sleep(0.05)
            
        if simvcd:
            simvcd.terminate()
        udpReader.terminate()
        
        log.debug('cycles=%s' % avr.cycle)
        log.debug('mcu time=%s' % avr.time_passed())
#        time.sleep(1)
        self.serial = udpReader.read()    
        
    def run(self):
        self.build()
        self.simulate()

    def get_serial(self):
        self.run()
        return self.serial
    
    def size(self):
        self.build()
        return self.cc.size()
    
#def targets():
#    return Avr.arduino_targets
#
#
#
#def code2size(snippet, mcu):
#    return ArduinoSim(snippet=snippet, mcu=mcu).size()
#
#def code2ser(snippet, mcu):
#    return ArduinoSim(snippet=snippet, mcu=mcu).get_serial()


