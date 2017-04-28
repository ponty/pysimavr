from mock import Mock
#from unittest.mock import Mock
from pyavrutils import AvrGcc
from pysimavr.avr import Avr
from pysimavr.firmware import Firmware
from pysimavr.swig.simavr import avr_raise_irq, IRQ_FLAG_FILTERED
import pysimavr.swig.utils as utils
from hamcrest import assert_that, equal_to, close_to

def _create_avr(mcu, f_cpu, code):
    cc = AvrGcc(mcu=mcu)
    cc.build(code)
    fw = Firmware(cc.output)
    return Avr(mcu=mcu, firmware=fw, f_cpu=f_cpu)

def test_io_irq():
    mcu = 'attiny2313'
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

    callbackMock = Mock()
    avr = _create_avr(mcu, 8000000, code)

    avr.irq.ioport_register_notify(callbackMock, ('B', 5))

    avr.step(10000)

    assert_that(callbackMock.call_count, equal_to(2), "Number of IRQ callback invocations.")
    avr.terminate()

def test_adc_irq():
    mcu = 'atmega2560'
    feedmv = 2400  # 2.4 volts

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
    avr = _create_avr(mcu, 4000000, code)

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

def test_pwm_irq():
    mcu = 'attiny44'
    code = '''
    #include <avr/io.h>
    #include <avr/interrupt.h>

    int main(){
        DDRB |= 1 << PORTB2;//PB2 output. Shared with OC0A.

        //8 bit timer. Fast PWM mode "3".

        TCCR0A|= (1 << WGM01) | (1 << WGM00);
        TCCR0A|=(1 << COM0A1) | (0 << COM0A0);//Noninverting mode. Clear OC0A on Compare Match, Set at bottom.         
        TCCR0B|=(1 << CS02)|(0 << CS01)|(0 << CS00);//256 prescaler. Internal clock

        OCR0A = 222;

        while(1);
     }
    '''

    avr = _create_avr(mcu, 1000000, code)
    callbackMock = Mock()
    avr.irq.timer_register_notify(callbackMock)
    avr.step(10000)

    assert_that(callbackMock.call_count, equal_to(1), "Number of IRQ callback invocations.")
    lastCallSecondArg = callbackMock.call_args[0][1]
    assert_that(lastCallSecondArg, equal_to(222), "OCR0A value.")
    avr.terminate()

def test_spi_irq():
    mcu = 'atmega48'
    # The code just sets one pin an output and pulse the digial IO
    code = '''
    #include <avr/io.h>

    int main(){
        SPCR = (1<<SPE)|(1<<MSTR)|(1<<SPR0); // Enable SPI, Master, set clock rate fck/16
        SPDR = 123;// Start transmission. Send 123.
        while(1);
    }
    '''
    avr = _create_avr(mcu, 8000000, code)
    callbackMock = Mock()
    avr.irq.spi_register_notify(callbackMock)

    avr.step(10000)

    assert_that(callbackMock.call_count, equal_to(1), "Number of IRQ callback invocations.")
    lastCallSecondArg = callbackMock.call_args[0][1]
    assert_that(lastCallSecondArg, equal_to(123), "Received SPI byte.")
    avr.terminate()

def test_uart_irq():
    mcu = 'atmega2560'
    code = '''
    #include <avr/io.h>

    int main() {
        UCSR3C = (3 << UCSZ30); //Async, no parity, 1 stop bit, 8 data bits, Transmit on rising XCK
        UCSR3B = (1 << TXEN3); //Enable transmitter only. No interrupts.
        UDR3 = 123;//Send one byte

        while(1);
    }
    '''
    avr = _create_avr(mcu, 8000000, code)
    callbackMock = Mock()
    avr.irq.uart_register_notify(callbackMock, 3, utils.UART_IRQ_OUTPUT)

    avr.step(10000)

    assert_that(callbackMock.call_count, equal_to(1), "Number of IRQ callback invocations.")
    lastCallSecondArg = callbackMock.call_args[0][1]
    assert_that(lastCallSecondArg, equal_to(123), "Received UART byte.")
    avr.terminate()
