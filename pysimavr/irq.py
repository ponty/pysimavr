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

    def _keep_alive(self, irqcb):
        self._avr_ref().callbacks_keepalive.append(irqcb)
        
    def _register_callback(self, irq_t, callback, keep_alive):
        irqcb = IRQCallback(irq_t, callback)
        if keep_alive:
            self._keep_alive(irqcb)
        return irqcb;

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

    def ioport_register_notify(self, callback, portPin, keep_alive=True):
        """ Register Digital IO port notification callback. 
        Triggered each time the digital output port changes its state. Like value, direction or similar.

        :param callback: A `callable(irq, newVal)`. See :func:`IRQCallback.on_notify`.
        :param portPin: See the :func:`IRQHelper.getioport`.
        :param keep_alive: See the :class:`IRQHelper`.
        :return: A :class:`~pysimavr.irq.IRQCallback` instance.
        """
        irq_t = self.getioport(portPin)
        return self._register_callback(irq_t, callback, keep_alive)

    def getadc(self, irqCtl):
        """ Analog to Digital Converter IRQ.

        :param irqCtl: The ADC IRQ type. One of the `pysimavr.swig.utils.AVR_IOCTL_ADC_*` constants.
        :return: An :class:`~pysimavr.swig.simavr.avr_irq_t` instance.
        """
        return avr_io_getirq(self._avrbackend, utils.AVR_IOCTL_ADC_GETIRQ, irqCtl)

    def adc_register_notify(self, callback, ctl=utils.ADC_IRQ_OUT_TRIGGER, keep_alive=True):
        """ Register ADC notification callback. 
        Triggered when the ADC is started in code. To feed the ADC with a value another ADC IRQ
        must be triggered using the :func:`~pysimavr.swig.simavr.avr_raise_irq` function.

        :param callback: A `callable(irq, newVal)`. See :func:`IRQCallback.on_notify`.
        :param ctl: See the :func:`IRQHelper.getadc`.
        :param keep_alive: See the :class:`IRQHelper`.
        :return: A :class:`~pysimavr.irq.IRQCallback` instance.
        """
        irq_t = self.getadc(ctl)
        return self._register_callback(irq_t, callback, keep_alive)

    def gettimer(self, timer_num, ctl):
        """ Timer IRQ. For PWM, scheduling etc.

        :param timer_num: Which timer/counter to use. For example `0` indicates `Timer/Counter0`. 
        :param ctl: The Timer IRQ type. One of the `pysimavr.swig.utils.AVR_TIMER_*` or `pysimavr.swig.utils.TIMER_IRQ_OUT_*` constants.
        :return: An :class:`~pysimavr.swig.simavr.avr_irq_t` instance.
        """
        return avr_io_getirq(self._avrbackend, utils.AVR_IOCTL_TIMER_GETIRQ(str(timer_num)) , ctl)

    def timer_register_notify(self, callback, timer_num=0, ctl=utils.TIMER_IRQ_OUT_PWM0, keep_alive=True):
        """ Register Timer notification callback. 
        To recover the PWD duty cycle register callback for one of the `TIMER_IRQ_OUT_PWMx` Timer IRQ type. The `newVal` parameter
        would then contain the value of the `OCRnx` register.

        :param callback: A `callable(irq, newVal)`. See :func:`IRQCallback.on_notify`.
        :param ctl: See the :func:`IRQHelper.gettimer`.
        :param keep_alive: See the :class:`IRQHelper`.
        :return: A :class:`~pysimavr.irq.IRQCallback` instance.
        """
        irq_t = self.gettimer(str(timer_num), ctl)
        return self._register_callback(irq_t, callback, keep_alive)

    def getspi(self, spi_num, ctl):
        """ SPI IRQ. 

        :param spi_num: Which SPI interface to use. For devices with multiple SPIs.  
        :param ctl: The SPI IRQ type. One of the `pysimavr.swig.utils.SPI_IRQ_*` constants.
        :return: An :class:`~pysimavr.swig.simavr.avr_irq_t` instance.
        """
        return avr_io_getirq(self._avrbackend, utils.AVR_IOCTL_SPI_GETIRQ(spi_num) , ctl)

    def spi_register_notify(self, callback, spi_num=0, ctl=utils.SPI_IRQ_OUTPUT, keep_alive=True):
        """ Register ADC notification callback. 
        Triggered when the ADC is started in code. To feed the ADC with a value another ADC IRQ
        must be triggered using the :func:`~pysimavr.swig.simavr.avr_raise_irq` function.

        :param callback: A `callable(irq, newVal)`. See :func:`IRQCallback.on_notify`.
        :param spi_num: Which SPI interface to use. See the :func:`IRQHelper.getspi`.
        :param ctl: See the :func:`IRQHelper.getspi`.
        :param keep_alive: See the :class:`IRQHelper`.
        :return: A :class:`~pysimavr.irq.IRQCallback` instance.
        """
        irq_t = self.getspi(spi_num, ctl)
        return self._register_callback(irq_t, callback, keep_alive)

    def getuart(self, uart_num, ctl):
        """ UART IRQ. 

        :param uart_num: Which UART interface to use.
        :param ctl: The SPI IRQ type. One of the `pysimavr.swig.utils.UART_IRQ_*` constants.
        :return: An :class:`~pysimavr.swig.simavr.avr_irq_t` instance.
        """
        return avr_io_getirq(self._avrbackend, utils.AVR_IOCTL_UART_GETIRQ(str(uart_num)) , ctl)

    def uart_register_notify(self, callback, uart_num=0, ctl=utils.UART_IRQ_OUTPUT, keep_alive=True):
        """ Register ADC notification callback. 
        Triggered when the ADC is started in code. To feed the ADC with a value another ADC IRQ
        must be triggered using the :func:`~pysimavr.swig.simavr.avr_raise_irq` function.

        :param callback: A `callable(irq, newVal)`. See :func:`IRQCallback.on_notify`.
        :param uart_num: Which UART interface to use. See the :func:`IRQHelper.getuart`.
        :param ctl: See the :func:`IRQHelper.getuart`.
        :param keep_alive: See the :class:`IRQHelper`.
        :return: A :class:`~pysimavr.irq.IRQCallback` instance.
        """
        irq_t = self.getuart(uart_num, ctl)
        return self._register_callback(irq_t, callback, keep_alive)


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
