/*
 * IRQCallback.cpp
 *
 *  Created on: Mar 8, 2017
 *      Author: premik
 */

#include "IRQCallback.h"
#include "sim_irq.h"
#include <stdexcept>


//#include <iostream>


/*
* Connection between the simavr c callback to the c++ object. The C++ instance is being passed using the generic param argument.
*/
static void _IRQ_callback(struct avr_irq_t * irq, uint32_t value, void * param) {
	//std::cout << "Callback " << std::endl;
	IRQCallback* cb = (IRQCallback*) param;
	cb->on_notify(irq, value);
}

IRQCallback::IRQCallback(struct avr_irq_t* irq) {
	this->irq = irq;
	avr_irq_register_notify(irq, _IRQ_callback, this);
}

struct avr_irq_t* IRQCallback::get_irq() {
	return this->irq;
}

IRQCallback::~IRQCallback() {
	//std::cout << "Destructor " << std::endl;
	avr_irq_unregister_notify(this->irq, _IRQ_callback, this);
}


void IRQCallback::on_notify(struct avr_irq_t* irq, uint32_t value) {
	//When used a pure virtual somehow it is not possible to init the class from python.
	//As the swig wrapper still thinks the class is abstract despite it was extended from python. 
	throw std::runtime_error("Virtual method on_notify is not implemented.");
	//std::cout << "Not implemented" << std::endl;
}
