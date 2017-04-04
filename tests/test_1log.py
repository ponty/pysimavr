from mock import Mock
#from unittest.mock import Mock
from pysimavr.avr import Avr
from nose.tools import eq_
from pysimavr.swig.simavr import cpu_Running 
import time


from pysimavr import logger

def test_custom_logger():
    loggerMethod = Mock()
    #Register custom callback method for simav logs
    logger.init_simavr_logger(loggerMethod)
    avr = Avr(mcu='atmega48', f_cpu=8000000)
    #Let the simavr run in background until it sadly crashes on ramend
    avr.run() 
    while avr.cycle < 8000 and avr.state == cpu_Running :
        time.sleep(0.1)
        
    # Expected:
    #('Starting atmega48 - flashend 0fff ramend 02ff e2end 00ff\n', 3)
    #('atmega48 init\n', 3)
    #('atmega48 reset\n', 3)
    #('avr_sadly_crashed\n', 1)
    eq_(loggerMethod.call_count, 4, "number of callback invocations")
    loggerMethod.assert_called_with('avr_sadly_crashed\n', 1)    
    avr.terminate()
