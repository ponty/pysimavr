from pysimavr.proxy import Proxy
from pyavrutils.avrsize import AvrSize
from pysimavr.logger import init_simavr_logger, get_simavr_logger
from pysimavr.uart import Uart
from pysimavr.timer import Timer
from pysimavr.swig.simavr import avr_make_mcu_by_name, avr_init, avr_start_thread, \
    avr_load_firmware, avr_run, avr_step_thread, avr_io_getirq, \
    AVR_IOCTL_IOPORT_GETIRQ, avr_peek, avr_fpeek, avr_continue_thread, \
    avr_pause_thread, avr_thread_goto_cycle, avr_terminate_thread, avr_terminate, \
    avr_reset
import pysimavr.swig.utils as utils
from pysimavr.irq import IRQHelper
import logging
import time

log = logging.getLogger(__name__)


class UnkwownAvrError(Exception):
    pass


class Avr(Proxy):
    _reserved = '''uart f_cpu arduino_targets avcc vcc avrsize reset mcu time_marker move_time_marker terminate goto_cycle 
                goto_time time_passed load_firmware step step_time step_cycles getirq fpeek peek run pause states firmware 
                timer callbacks_keepalive irq'''.split()
    arduino_targets = 'atmega48 atmega88 atmega168 atmega328p'.split()

    states = [
        'Limbo',  # before initialization is finished
        'Stopped',  # all is stopped, timers included
        'Running',  # we're free running
        'Sleeping',  # we're now sleeping until an interrupt
        'Step',  # run ONE instruction, then...
        'StepDone',  # tell gdb it's all OK, and give it registers,
        'Done',  # avr software stopped gracefully
        'Crashed'  # avr software crashed (watchdog fired)
    ]

    def __init__(self, firmware=None, mcu=None, f_cpu=None, avcc=5, vcc=5):
        '''

        :param mcu: mcu name
        :param f_cpu: frequency in hertz
        :param avcc: avcc in Volt
        :param vcc: vcc in Volt
        '''
        if get_simavr_logger() is None:
            init_simavr_logger()  # Only init logger when it was not initialized before
        self.callbacks_keepalive = [] # External callback instances are stored here just to avoid GC destroying them too early
        self._irq_helper = IRQHelper(self)
        self.avrsize = None
        self.time_marker = 0.0
        self.mcu = mcu
        self.f_cpu = f_cpu
        self._avcc = avcc
        self._vcc = vcc

        if firmware:
            if not self.mcu:
                self.mcu = str(firmware.mcu)
            if not self.f_cpu:
                self.f_cpu = firmware.frequency

        assert self.mcu
        assert self.f_cpu

        log.debug('mcu=%s f_cpu=%s' % (self.mcu, self.f_cpu))

        self.backend = avr_make_mcu_by_name(self.mcu)
        if not self.backend:
            raise UnkwownAvrError('unknown AVR: ' + self.mcu)

        avr_init(self.backend)
        self.backend.frequency = self.f_cpu  # Propagate the freq to the backend

        self._set_voltages()

        avr_start_thread(self.backend)
        self.pause()
        if firmware:
            self.load_firmware(firmware)
        self.uart = Uart(self)
        self.uart.connect()

    def load_firmware(self, firmware):
#        avr_terminate_thread()
        self.pause()
        #  TODO: remove sleep
        # otherwise crash by reload
        time.sleep(0.5)

        self.avrsize = AvrSize()
        self.avrsize.run(firmware.filename, self.mcu)

        self.reset()
        self.firmware = firmware
        firmware.mcu = self.mcu
        firmware.frequency = self.f_cpu
        avr_load_firmware(self.backend, firmware.backend)
        self._set_voltages()

    def _set_voltages(self):
        self.backend.avcc = int(self._avcc * 1000)
        self.backend.vcc = int(self._vcc * 1000)

    @property
    def avcc(self):
        return self._avcc

    @property
    def vcc(self):
        return self._vcc

    @avcc.setter
    def avcc(self, v):
        self._avcc = v
        self._set_voltages()

    @vcc.setter
    def vcc(self, v):
        self._vcc = v
        self._set_voltages()

    def __del__(self):
        self.terminate()

    _terminated = False

    def terminate(self):
        if self._terminated:
            return
        self._terminated = True
        log.debug('terminating...')
        # Release references to all callbacks kept-alive so they can get GC collected. 
        self.callbacks_keepalive = []
        avr_terminate_thread()
        avr_terminate(self.backend)
        self.uart.terminate()
        log.debug('...ok')

    def step(self, n=1, sync=True):
        if sync:
            for _ in range(n):
                avr_run(self.backend)
        else:
            # asynchrone
            avr_step_thread(n)

#    def step_time(self, tsec):
#        self.step_cycles(tsec * self.f_cpu)
#
#    def step_cycles(self, n):
#        avr_thread_step_cycles(self.backend, int(n))

    def goto_time(self, tsec):
        self.goto_cycle(tsec * self.f_cpu)

    def move_time_marker(self, tsec_diff):
        self.time_marker += tsec_diff
        self.goto_time(self.time_marker)

    def goto_cycle(self, n):
        avr_thread_goto_cycle(self.backend, int(n))

    def time_passed(self):
        return 1.0 * self.backend.cycle / self.f_cpu

    def _getirq(self, port, pin):
        return avr_io_getirq(self.backend, AVR_IOCTL_IOPORT_GETIRQ(port), pin)

    def getirq(self, pin):
        '''
        deprecated:: 0.2.3
        Use :method:`irq.getioport` instead.
        '''
        return self._getirq(pin[0], int(pin[1]))

    @property
    def irq(self):
        return self._irq_helper;

    def peek(self, addr):
        if addr >= self.backend.ramend:
            raise Exception(
                'addr(%s) >= ramend(%s)' % (addr, self.backend.ramend))
        return avr_peek(self.backend, addr)

    def fpeek(self, addr):
        if addr >= self.backend.flashend:
            raise Exception(
                'addr(%s) >= flashend(%s)' % (addr, self.backend.flashend))
        return avr_fpeek(self.backend, addr)

    def run(self):
        avr_continue_thread()

    def pause(self):
        avr_pause_thread()

    def reset(self):
        self.time_marker = 0.0
        self.goto_cycle(0)
        avr_reset(self.backend)
        self.backend.cycle = 0  # no reset in simavr !

    def timer(self, callback, cycle=0, uSec=0, keep_alive=True):
        """Registers a new cycle timer callback. Use either `cycle` or `uSec` parameter to schedule the notification.

        :param callback: The callback function. A `callable(when)->int`. See :func:`Timer.on_timer <pysimavr.timer.Timer.on_timer>` for more details.
        :param cycle: When the callback should be invoked. The simavr mcu cycle number.
        :param uSec: When the callback should be invoked. The virtual time from mcu startup in micro-seconds. Gets converted to cycles internally.. 
        :param keep_alive: Whether the returned object should be referenced internally. See the :class:`~pysimavr.irq.IRQHelper` for more details.

        :return: A :class:`~pysimavr.timer.Timer` instance.   
        """
        t = Timer(self, callback)
        if keep_alive:
            self.callbacks_keepalive.append(t)
        if cycle > 0: 
            t.set_timer_cycles(cycle)
        if uSec > 0: 
            t.set_timer_usec(uSec)
        return t
