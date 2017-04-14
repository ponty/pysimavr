from pysimavr.swig.utils import LoggerCallback
from pysimavr.swig.simavr import LOG_OUTPUT, LOG_ERROR, LOG_WARNING, LOG_TRACE
import logging
import traceback

log = logging.getLogger(__name__)

simavr_to_py_log_level = {
        LOG_OUTPUT:logging.FATAL,
        LOG_ERROR:logging.ERROR, 
        LOG_WARNING:logging.WARNING,
        LOG_TRACE:logging.DEBUG        
}


def pylogging_log(line, avr_log_level):
    """The default logging function utilising the python logging framework."""
    py_log_level = simavr_to_py_log_level.get(avr_log_level, logging.DEBUG )
    if not log.isEnabledFor(py_log_level): return;        
    log.log(py_log_level, line.strip());


class SimavrLogger(LoggerCallback):
    """Consumes log statements from the core simavr logger and propagates
    them to the configured callback function. The default callback function is using 
    the `pylogging_log` which uses python logging.
    
    Do not create instance of this class directly but use the provided `init_simavr_logger` module function instead. 
    """  

       
    def __init__(self, callback=None):
        LoggerCallback.__init__(self)
        #super(TimerCallback, self).__init__()
        self._callback = callback
        
    def on_log(self, line, avr_log_level):
        if self._callback:
            try: self._callback(line, avr_log_level)
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
        
def get_simavr_logger():
    if  '_simavr_logger' in globals():
        return globals()['_simavr_logger']
    return None 


def init_simavr_logger(logger=pylogging_log):
    """Sets the logger callback. Use to redirect logs to a custom handler.
    
    When using a custom logging function it is necessary to set the custom logger
    before the `pysimavr.avr.Avr` is created. Otherwise some of the early simavr simavr log 
    messages might get missed.
    
    Note the `avr_log_level` withe zero value (`pysimavr.swig.simavr.LOG_OUTPUT`) indicates the message is
    an output for the simulated firmware. 
    """  
    global _simavr_logger
    _simavr_logger = get_simavr_logger()
    if logger is None:
        _simavr_logger = None
        return
    if _simavr_logger is None:
        _simavr_logger = SimavrLogger()
    _simavr_logger.callback = logger