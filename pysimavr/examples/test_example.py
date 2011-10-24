''' unit test example'''

from pysimavr.sim import ArduinoSim

def test_atmega88():
    mcu = 'atmega88'
    snippet = 'Serial.print("hi");'
    
    output = ArduinoSim(snippet=snippet, mcu=mcu, timespan=0.01).get_serial()
    assert output == 'hi'
