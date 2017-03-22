from mock import Mock
#from unittest.mock import Mock

from nose.tools import eq_
from pysimavr.avr import Avr
from pysimavr.swig.simavr import cpu_Running 


def test_timer_simple():
    avr = Avr(mcu='atmega88', f_cpu=8000000)    
    # Callback method mocked out. 
    callbackMock = Mock(return_value=0)
    
    #Schedule callback at 20uSec.  
    # cycles = avr->frequency * (avr_cycle_count_t)usec / 1000000;
    timer = avr.timer(callbackMock, uSec=20)
    expectedCycle = 8000000*20/1000000
    
    # Check uSec got converted to cycles correctly. 
    assert abs(expectedCycle-timer.status()) < 10
    
    avr.step(1000)
    eq_(avr.state, cpu_Running, "mcu is not running")
            
    eq_(callbackMock.call_count, 1, "number of calback invocations")
    avr.terminate()

def test_timer_reoccuring():        
    avr = Avr(mcu='atmega48', f_cpu=8000000)
    # Callback method mocked out. It will register another callback 
    # at 200 cycles and then cancel by returning 0.
    callbackMock = Mock(side_effect = [200, 0])
    
    timer = avr.timer(callbackMock)
    avr.step(10)
    eq_(avr.state, cpu_Running, "mcu is not running")
    callbackMock.assert_not_called()
    
    # Request first timer callback at 100 cycles
    timer.set_timer_cycles(100)    
    
    # Run long enought to ensure callback is canceled by returning 0 on the second invocation.
    avr.step(1000)
    eq_(avr.state, cpu_Running, "mcu is not running")
    eq_(callbackMock.call_count, 2, "number of calback invocations")
        
    lastCallFirstArg = callbackMock.call_args[0][0]
    
    #Check the last cycle number received +- matches the requested one 
    assert abs(lastCallFirstArg-200) < 10
    avr.terminate()
    
def test_timer_cancel():
    avr = Avr(mcu='atmega88', f_cpu=1000000)
    callbackMock = Mock(return_value=200)
    timer = avr.timer(callbackMock, cycle=50)    
    avr.step(10)
    callbackMock.assert_not_called()
    
    timer.cancel()
    avr.step(1000)
    callbackMock.assert_not_called()    
         
    avr.terminate()