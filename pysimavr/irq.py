from pysimavr.swig.utils import IRQCallback as _IRQCallback
from pysimavr.swig.simavr import avr_io_getirq
import pysimavr.swig.utils as utils
import traceback
import weakref

class IRQHelper(object):
    """ Helper methods related to simavr IRQ functionality. Closely coupled with the
    main :class:`~pysimavr.avr.Avr` instance. There is no need to create instance of this class directly since there is 
    a pre-created one available already. Use the :attr:`avr.irq <pysimavr.avr.Avr.irq>` to access it.

    All the **get...** methods return the :class:`~pysimavr.swig.simavr.avr_irq_t` instance and wrap various 
    simavr `AVR_IOCTL_IOPORT_...` macros in convenient way.

    All the **...register_notify** methods registers the provided callback function via the :class:`IRQCallback`. See 
    the :func:`IRQCallback.on_notify` method for the callback function signature and more details.

    The optional **keepAlive** parameter indicates the ownership of the returned  :class:`IRQCallback` object.
    By default it is **True** which means there is an additional reference being held internally. That way the callback object
    is not destroyed sooner than the main :class:`~pysimavr.avr.Avr` instance. 
    When the `keepAlive` is set to `False` it is the callers responsibility to keep the returned object referenced for the desired lifetime
    of the notifications.
    """

    def __init__(self, avr):
        self._avr_ref = weakref.ref(avr)

    def _keepAlive(self, irqcb):
        self._avr_ref().callbacks_keepalive.append(irqcb)

    @property
    def _avrbackend(self):
        return self._avr_ref().backend

    def getioport(self, portPin):
        """ Digital IO IRQ.

        :param portPin: `(port, pin)` tuple.
            The port is a single uppercase character like `"A"`.
            The pin is one of the `pysimavr.swig.utils.IOPORT_IRQ_*` constants. For example `("A", IOPORT_IRQ_PIN_ALL)` tuple represents
            all the 8 bits of the port. Note the `IOPORT_IRQ_PINx' constants are intentionally declared with values `0..7` in simavr.
            So it is possible to use plain integers to address a specific pin of a port too. For example `("A", 6)` indicates *A6* port.
        :return: An :class:`~pysimavr.swig.simavr.avr_irq_t` instance.
        """
        return avr_io_getirq(self._avrbackend, utils.AVR_IOCTL_IOPORT_GETIRQ(portPin[0]), int(portPin[1]))

    def ioport_register_notify(self, callback, portPin, keepalive=True):
        """ Register Digital IO port notification callback. 
        Triggered each time the digital output port changes its state. Like value, direction or similar.

        :param callback: A `callable(irq, newVal)`. See :func:`IRQCallback.on_notify`.
        :param portPin: See the :func:`IRQHelper.getioport`.
        :param keepalive: See the :class:`IRQHelper`.
        :return: A :class:`~pysimavr.irq.IRQCallback` instance.
        """
        irq_t = self.getioport(portPin)
        irqcb = IRQCallback(irq_t, callback)
        if keepalive:
            self._keepAlive(irqcb)
        return irqcb;

    def getadc(self, irqIndex):
        """ Analog to Digital Converter IRQ.

        :param irqIndex: The ADC IRQ type. One of the `pysimavr.swig.utils.AVR_IOCTL_ADC_*` constants.
        :return: An :class:`~pysimavr.swig.simavr.avr_irq_t` instance.
        """
        return avr_io_getirq(self._avrbackend, utils.AVR_IOCTL_ADC_GETIRQ, irqIndex)

    def adc_register_notify(self, callback, irqIndex=utils.ADC_IRQ_OUT_TRIGGER, keepalive=True):
        """ Register ADC notification callback. 
        Triggered when the ADC is started in code. To feed the ADC with a value another ADC IRQ
        must be triggered using the :func:`~pysimavr.swig.simavr.avr_raise_irq` function.

        :param callback: A `callable(irq, newVal)`. See :func:`IRQCallback.on_notify`.
        :param portPin: See the :func:`IRQHelper.getioport`.
        :param keepalive: See the :class:`IRQHelper`.
        :return: A :class:`~pysimavr.irq.IRQCallback` instance.
        """
        irq_t = self.getadc(irqIndex)
        irqcb = IRQCallback(irq_t, callback)
        if keepalive:
            self._keepAlive(irqcb)
        return irqcb;

class IRQCallback(_IRQCallback):
    """ Wraps the simavr IRQ notifications which can be used to
    receive events from the simulated avr and other attached parts.

    Note when this object is destroyed the notification is unregistered automatically.
    """

    def __init__(self, irq,  callback=None):
        _IRQCallback.__init__(self, irq)
        self._callback = callback
        #super(TimerCallback, self).__init__()

    def on_notify(self, irq, newVal):
        """ The callback method called from simavr.

        :param irq: The original :class:`~pysimavr.swig.simavr.avr_irq_t` object this listener was registered with. Note
            the `irq.value` contains the previous value.
        :param newVal: An arbitrary integer parameter provided as part of the event. The real meaning is IRQ specific. For example it
            could be `1, 0` for digital pins or an analog value (in milivolts) for ADC.
        """
        if self._callback:
            try: return self._callback(irq, newVal)
            except:
                #Log any python exception here since py stacktrace is not propagated down to C++ and it would be lost.
                traceback.print_exc()
                raise

    @property
    def callback(self):
        return self._callback;

    @callback.setter
    def callback(self, callback):
        self._callback = callback
