from _weakref import proxy

from pysimavr.proxy import Proxy

from pysimavr.swig.utils import TimerCallback


class Timer(TimerCallback):
    """Wraps the simavr cycle_timer functionality. Enables to hook a python method
    to be called every x simavr cycles. 
    """
        
    
    def __init__(self, avr, callback=None):
        TimerCallback.__init__(self, avr)
        #super(TimerCallback, self).__init__()
        self._callback = callback
        
     
        
    
    def on_timer(self, when):
        """ The callback called from simavr.
        :Parameters:
            `when` : The exact simavr cycle number. Note actual cycle number could be
                slightly off the requested one.
        :Returns: The new cycle number the next callback should be invoked. 
                Or zero to cancel the callback.           
        """
        if self._callback:
            # Cast to int since unrelying swig error would be cryptic
            return int(self._callback(when))
            
            
    @property
    def callback(self):
        return self._callback;
    
    @callback.setter
    def callback(self, callback):
        self._callback = callback
    