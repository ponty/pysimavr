/*
 * TimerCallback.cpp
 *
 *  Created on: Mar 8, 2017
 *      Author: premik
 */

#include "TimerCallback.h"
#include "sim_avr.h"
#include <exception>
#include <stdexcept>
#include <signal.h>

//#include <iostream>

/*
* Connection between the simavr c callback to the c++ object. The C++ instance is being passed using the generic param argument.
*/
static avr_cycle_count_t _timer_callback(struct avr_t* avr, avr_cycle_count_t when, void* param) {
	//AVR_LOG(avr, LOG_WARNING, "Callback\n");
	//std::cout << "Callback internal " << when << std::endl;
	TimerCallback* tc = (TimerCallback*) param;
	return tc->on_timer(when);
}

TimerCallback::TimerCallback(struct avr_t* avr) {
	this->avr = avr;
}

TimerCallback::~TimerCallback() {
	this->cancel();
}

void TimerCallback::set_timer_cycles(avr_cycle_count_t when) {
	avr_cycle_timer_register(this->avr, when, _timer_callback, this);
}

void TimerCallback::set_timer_usec(uint32_t when) {
	avr_cycle_timer_register_usec(this->avr, when, _timer_callback, this);
}

void TimerCallback::cancel() {
	avr_cycle_timer_cancel(this->avr, _timer_callback, this);
}

avr_cycle_count_t TimerCallback::status() {
	return avr_cycle_timer_status(this->avr, _timer_callback, this);
}

avr_cycle_count_t TimerCallback::on_timer(avr_cycle_count_t when) {
	//When used a pure virtual somehow it is not possible to init the class from python.
	//As the swig wrapper still thinks the class is abstract despite it was extended from python. 
	throw std::runtime_error("Virtual method on_timer is not implemented.");
	//std::cout << "Not implemented" << std::endl;
}