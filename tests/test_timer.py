from mock import Mock
#from unittest.mock import Mock

from nose.tools import eq_
from pysimavr.avr import Avr
from pysimavr.swig.simavr import cpu_Running 
from hamcrest import assert_that, close_to, equal_to, none, is_, not_none
import weakref
import gc

def test_timer_simple():
    avr = Avr(mcu='atmega88', f_cpu=8000000)
    # Callback method mocked out. 
    callbackMock = Mock(return_value=0)

    #Schedule callback at 20uSec.
    # cycles = avr->frequency * (avr_cycle_count_t)usec / 1000000;
    timer = avr.timer(callbackMock, uSec=20)

    assert_that(timer.status(), close_to(8000000*20/1000000, 10),
                "uSec to cycles convertion")

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
    assert_that(lastCallFirstArg, close_to(200, 10),
                "The last cycle number received in the callback doesn't match the requested one")
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

def test_timer_GC():
    avr = Avr(mcu='atmega88', f_cpu=1000000)
    callbackMock = Mock(return_value=0)
    #Don't let avr object to keep the callback referenced.
    t = weakref.ref(avr.timer(callbackMock, cycle=10, keep_alive=False))
    gc.collect()
    assert_that(t(), is_(none()), "Orphan Timer didn't get garbage collected.")
    avr.step(100)
    assert_that(callbackMock.call_count, equal_to(0), "Number of IRQ callback invocations.")

    #Now let avr object keep the callback alive.
    t = weakref.ref(avr.timer(callbackMock, cycle=110, keep_alive=True))
    gc.collect()
    assert_that(t(), is_ (not_none()), "Avr object didn't kept Timer callback alive.")
    avr.step(1000)
    assert_that(callbackMock.call_count, equal_to(1), "Number of IRQ callback invocations.")
    avr.terminate()
    gc.collect()
    assert_that(t(), is_(none()), "Orphan Timer didn't get garbage collected even after Avr is terminated.")
