from nose.tools import eq_
from pysimavr.avr import Avr
from pysimavr.sim import ArduinoSim

def test_udp():
    snippet='''
    for(int i=0;i<100;i++)
    {
        Serial.print(i);
        Serial.println(":abcdefgh");
        //delay(100);
    }
    '''
    x=ArduinoSim(snippet=snippet, timespan=2.5).get_serial()
    print x
    lines=x.splitlines()
    eq_(len(lines), 100)
    for i,l in zip(xrange(100),lines):
        eq_(l, str(i)+":abcdefgh")
    
