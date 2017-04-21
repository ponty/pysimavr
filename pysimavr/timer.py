from pysimavr.swig.utils import TimerCallback
import traceback

class Timer(TimerCallback):
    """ Wraps the simavr cycle_timer functionality. Enables to hook a python method
    to be called every x simavr cycles. 

    Note there is usually no need to create instance of this class directly as there is a 
    helper :func:`avr.timer <pysimavr.avr.Avr.timer>` method available.
    """

    def __init__(self, avr, callback=None):
        TimerCallback.__init__(self, avr)
        #super(TimerCallback, self).__init__()
        self._callback = callback


    def on_timer(self, when):
        """ The callback called from simavr.

        :param when: The exact simavr cycle number. Note actual cycle number could be
                slightly off the requested one.
        :return: The new cycle number the next callback should be invoked. 
                Or zero to cancel the callback.           
        """
        if self._callback:
            try: return self._callback(when)
            except:
                #Log any python exception here since py stacktrace is not propagated down to C++ and it would be lost
                traceback.print_exc()
                raise

    @property
    def callback(self):
        return self._callback;

    @callback.setter
    def callback(self, callback):
        self._callback = callback
