from pyavrutils.arduino import Arduino
from pysimavr.avr import Avr
from pysimavr.firmware import Firmware
from pysimavr.udp import Udp
from pysimavr.udpreader import UdpReader2
import logging

log = logging.getLogger(__name__)

TEMPLATE = '''
void setup()
{
    Serial.begin(9600);

    CODE_SNIPPET;
    
}

void loop()
{
}
'''

class ArduinoSimSerial(object):
    '''arduino code builder and simulator for serial testing'''
    def __init__(self,
                 code=None,
                 snippet=None,
                 mcu='atmega128',
                 f_cpu=16000000,
                 extra_lib=None):
        self.cc = Arduino(mcu=mcu, f_cpu=f_cpu, extra_lib=extra_lib)
        self.template = TEMPLATE
        self.snippet = snippet
        self.code = code
        self.time_to_go = 0.01 # 10ms
        
    def build(self):
        code = self.code
        if not code:
            code = self.template.replace('CODE_SNIPPET', self.snippet)
        log.debug('code=%s' % code)
        self.cc.build(code)

    def simulate(self):
        elf = self.cc.output
        
        # run
        firmware = Firmware(elf)
        self.avr = Avr(mcu=self.cc.mcu, f_cpu=self.cc.f_cpu)
        self.avr.load_firmware(firmware)
        udpReader = UdpReader2()
        udp = Udp(self.avr)
        udp.connect()
        udpReader.start()
        
        self.avr.move_time_marker(self.time_to_go)
        
        log.debug('cycles=%s' % self.avr.cycle)
        log.debug('mcu time=%s' % self.avr.time_passed())
        s = udpReader.read()    
        return s
        
    def serial(self):
        self.build()
        s = self.simulate()
        return s
    
    def size(self):
        self.build()
        return self.cc.size()
    
def targets():
    return Avr.arduino_targets



def code2size(code_snippet, mcu):
    return ArduinoSimSerial(snippet=code_snippet, mcu=mcu).size()

def code2ser(code_snippet, mcu):
    return ArduinoSimSerial(snippet=code_snippet, mcu=mcu).serial()


