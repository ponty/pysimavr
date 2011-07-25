#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "inverter.h"
#include "avr_ioport.h"

static void inverter_pin_changed_hook(struct avr_irq_t * irq, uint32_t value,
		void *param)
{
	inverter_t *b = (inverter_t *) param;

	value = !value;
	//printf("irq->irq=%d\n",irq->irq);
	b->out = value;
	//b->out_changed |= (1 << irq->irq);

	//int index = irq->irq;
//	printf("x=%x\n", b->irq);
//	printf("b=%x\n", b);
	avr_raise_irq(b->irq + IRQ_INVERTER_OUT, value);

}

static const char * irq_names[INVERTER_IRQ_COUNT] =
{ [IRQ_INVERTER_IN] = "<inverter.IN", //
		[IRQ_INVERTER_OUT] = "<inverter.OUT", //
		};

void inverter_core_init(struct avr_t *avr, struct inverter_t * b)
{
	memset(b, 0, sizeof(*b));
	b->avr = avr;

	/*
	 * Register callbacks on all our IRQs
	 */
	b->irq = avr_alloc_irq(&avr->irq_pool, 0, INVERTER_IRQ_COUNT, irq_names);
//	printf("xzzzzzx=%x\n", b->irq);
//	printf("bbbbb=%x\n", b);

	avr_irq_register_notify(b->irq + IRQ_INVERTER_IN,
			inverter_pin_changed_hook, b);
}

