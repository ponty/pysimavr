/*
 * IRQCallback.h
 *
 *  Created on: Mar 8, 2017
 *      Author: premik
 */

#ifndef UTILS_IRQCALLBACK_H_
#define UTILS_IRQCALLBACK_H_

#include "sim_irq.h"


/*
 * Enables IRQ notification function to be used with python method.
 * The simavr IRQs is a mean to register and propagate events among simavr components.
 *
 */
class IRQCallback {
public:
	IRQCallback(struct avr_irq_t* irq);
	virtual ~IRQCallback();
	virtual void on_notify(struct avr_irq_t* irq, uint32_t value);//Implement this one in Pyhton class.
	struct avr_irq_t* get_irq();

protected:
	struct avr_irq_t* irq;

};

#endif /* UTILS_IRQCALLBACK_H_ */
