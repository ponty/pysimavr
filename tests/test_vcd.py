from nose.tools import eq_
from pysimavr.avr import Avr
from pysimavr.sim import ArduinoSim
import tempfile

def test():
    snippet='''
        Serial.println("start");
        pinMode(0, OUTPUT);     
        digitalWrite(0, HIGH);   
        delay(100);           
        digitalWrite(0, LOW);   
        delay(100);              
        digitalWrite(0, HIGH);   
        delay(100);           
        digitalWrite(0, LOW);   
        delay(100);             
        Serial.println("end");
    '''
    vcdfile= tempfile.mkdtemp() + '/vcdtest.vcd'
    sim=ArduinoSim(snippet=snippet, vcd=vcdfile, timespan=0.5)
    sim.run()
