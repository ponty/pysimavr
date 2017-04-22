from mock import Mock
#from unittest.mock import Mock
from pyavrutils import AvrGcc
from pysimavr.avr import Avr
from pysimavr.firmware import Firmware
from pysimavr.swig.simavr import avr_raise_irq, IRQ_FLAG_FILTERED
import pysimavr.swig.utils as utils
from hamcrest import assert_that, equal_to, close_to

def test_io_irq():
    mcu = 'attiny2313'
    cc = AvrGcc(mcu=mcu)
    # The code just sets one pin an output and pulse the digial IO
    code = '''
    #include <avr/io.h>

    int main(){
        PORTB|=  _BV(PORTB5); //B5 pullup. To avoid possible oscilation on DD change
        DDRB |=  _BV(DDB5);   //B5 output
        PORTB|=  _BV(PORTB5); //B5 high
        PORTB&= ~_BV(PORTB5); //B5 low
        while(1); //Avoid ramend run out. Although gcc probably generates this already.
    }
    '''

    cc.build(code)
    fw = Firmware(cc.output)

    callbackMock = Mock()

    avr = Avr(mcu=mcu, firmware=fw, f_cpu=8000000)
    avr.irq.ioport_register_notify(callbackMock, ('B', 5))

    avr.step(10000)

    assert_that(callbackMock.call_count, equal_to(2), "Number of IRQ callback invocations.")
    avr.terminate()

def test_adc_irq():
    mcu = 'atmega2560'
    feedmv = 2400  # 2.4 volts

    cc = AvrGcc(mcu=mcu)
    # The code do one ADC and "sends" the captured value back as 16bit number using the A and B ports
    code = '''
    #include <avr/io.h>

    int main(){
        DDRB =  0xFF;   //A output
        DDRA =  0xFF;   //B output

        //Init ADC
        ADMUX = (1 << MUX1)| (1 << REFS0);// Select MUTEX to ADC2, and VCC reference
        ADCSRB = 0;
        //Set 64 Prescaler division = (125khz @ 8MHZ clock) and enable.
        ADCSRA = (1 << ADEN) |(1 << ADPS2) | (1 << ADPS1) | (0 << ADPS0);
        ADCSRA|= (1 << ADSC); //Start conversion. Single Conversion mode.
        while (ADCSRA & (1 << ADSC)); //Wait for the conv. to finish

        //Use all the bits of the port A and B to "send" the converted value back to the test.
        PORTB = ADCL;
        PORTA = ADCH;

        while(1);
    }
    '''

    cc.build(code)
    fw = Firmware(cc.output)
    avr = Avr(mcu=mcu, firmware=fw, f_cpu=4000000)

    # Called once AVR starts the ADC.
    def adcCallback(irq, newVal):
        # Feed the analog value (in milivolts) to the ADC2.
        irq_t = avr.irq.getadc(utils.ADC_IRQ_ADC2)
        avr_raise_irq(irq_t, feedmv)

    # Wrap further to Mock object to enable recording the number of calls.
    adcCallbackMock = Mock(side_effect=adcCallback)
    avr.irq.adc_register_notify(adcCallbackMock)

    # The result value "sent" back from simulated code. Need to wrap the variable into an array 
    # to workaround the "referenced before assignment" errors.
    result = [0]  

    # Called each time A or B port is changed
    def portCallback(irq, newVal):
        if irq.name[0] == 'A':
            newVal = newVal << 8
        result[0] += newVal

    portCallbackMock = Mock(side_effect=portCallback)

    for port in ('A', 'B'):
        p = avr.irq.ioport_register_notify(portCallbackMock, (port, utils.IOPORT_IRQ_PIN_ALL))
        p.get_irq().name = port  # Rename the IO IRQs to ease the Word recomposition in the callback
        # Force callback even on unchanged port values. Just to always have the same number of callback calls.
        p.get_irq().flags &= ~IRQ_FLAG_FILTERED 

    avr.step(10000)

    assert_that(adcCallbackMock.call_count, equal_to(1), "Number of ADC trigger_out callback invocations.")

    # The port A and B callback gets triggeret at startup first when they are set to output. Two 0 values are sent. 
    # And later when the result value is being send back. Hence 4x.     
    assert_that(portCallbackMock.call_count, equal_to(4), "Number of IO IRQ callback invocations.")
    expectedAdc = avr.vcc * 1000 * result[0] / 1024  # 10 bit ADC. VCC used as vref.
    assert_that(expectedAdc, close_to(feedmv, 10), "ADC result")

    avr.terminate()
