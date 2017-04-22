%module(directors="1") utils
%include "constraints.i"

// *********************************
// * Callbacks                     *
// *********************************
%{
#include "TimerCallback.h"
#include "LoggerCallback.h"
#include "IRQCallback.h"
%}


// Enable cross-language polymorphism in the SWIG wrapper. 
%feature("director") TimerCallback;
%feature("director") LoggerCallback;
%feature("director") IRQCallback;

//avr_cycle_count_t => uint64_t
%apply unsigned long long { avr_cycle_count_t }
%apply unsigned long { uint32_t }
%apply Pointer NONNULL { avr_t* };
%apply Pointer NONNULL { avr_irq_t* };

%ignore instance; //LoggerCallback* LoggerCallback::instance 

%include "TimerCallback.h"
%include "LoggerCallback.h"
%include "IRQCallback.h"

// *********************************
// * IRQs                          *
// *********************************
%{
#include "avr_adc.h"
#include "avr_eeprom.h"
#include "avr_extint.h"
#include "avr_flash.h"
#include "avr_ioport.h"
#include "avr_spi.h"
#include "avr_timer.h"
#include "avr_twi.h"
#include "avr_uart.h"
#include "avr_usb.h"
#include "avr_watchdog.h"
%}

long AVR_IOCTL_DEF(char, char, char, char);
%constant long AVR_IOCTL_ADC_GETIRQ;
%constant long AVR_IOCTL_EEPROM_GET;
%constant long AVR_IOCTL_EEPROM_SET;
long AVR_IOCTL_EXTINT_GETIRQ();
%constant long AVR_IOCTL_FLASH_SPM;
%constant long AVR_IOCTL_IOPORT_GETIRQ_REGBIT;
long AVR_IOCTL_IOPORT_GETIRQ(char);
long AVR_IOCTL_IOPORT_GETSTATE(char);
long AVR_IOCTL_IOPORT_SET_EXTERNAL(char);
long AVR_IOCTL_SPI_GETIRQ(char);
long AVR_IOCTL_TIMER_GETIRQ(char);
long AVR_IOCTL_TIMER_SET_TRACE(char);
long AVR_IOCTL_TWI_GETIRQ(char);
long AVR_IOCTL_UART_GET_FLAGS(char);
long AVR_IOCTL_UART_GETIRQ(char);
long AVR_IOCTL_UART_SET_FLAGS(char);
long AVR_IOCTL_USB_GETIRQ();
%constant long AVR_IOCTL_USB_READ;
%constant long AVR_IOCTL_USB_RESET;
%constant long AVR_IOCTL_USB_SETUP;
%constant long AVR_IOCTL_USB_VBUS;
%constant long AVR_IOCTL_USB_WRITE;
%constant long AVR_IOCTL_WATCHDOG_RESET;



%include "avr_adc.h"
%include "avr_eeprom.h"
%include "avr_extint.h"
%include "avr_flash.h"
%include "avr_ioport.h"
%include "avr_spi.h"
%include "avr_timer.h"
%include "avr_twi.h"
%include "fifo_declare.h"
%include "avr_uart.h"
%include "avr_usb.h"
%include "avr_watchdog.h"