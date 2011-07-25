#ifndef __INVERTER_CORE_H__
#define __INVERTER_CORE_H__

#include "sim_irq.h"


enum
{
	IRQ_INVERTER_IN,
	IRQ_INVERTER_OUT,

	INVERTER_IRQ_COUNT,
};

typedef struct inverter_t
{
	avr_irq_t * irq;
	struct avr_t * avr;

	int out;
	//uint64_t out_changed;

} inverter_t;

void inverter_core_init(struct avr_t *avr, struct inverter_t * b);


#endif 
