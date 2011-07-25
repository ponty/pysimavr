#include <stdlib.h>
#include <stdio.h>
#include <string.h>
//#include "sim_cycle_timers.h"
#include "ledrow.h"
#include "avr_ioport.h"
//#include "sim_vcd_file.h"

static void ledrow_pin_changed_hook(struct avr_irq_t * irq, uint32_t value,
		void *param)
{
	ledrow_t *b = (ledrow_t *) param;

	//printf("ledrow=%d\n", value);

	b->pinstate = (b->pinstate & ~(1 << irq->irq)) | (value << irq->irq);
	b->pinstate_changed |= (1 << irq->irq);
}

static const char * irq_names[LEDROW_MAX_PIN_COUNT] =
{ [IRQ_LEDROW_PIN] = "<ledrow.0", //
		[IRQ_LEDROW_PIN + 1] = "<ledrow.1", //
		[IRQ_LEDROW_PIN + 2] = "<ledrow.2", //
		[IRQ_LEDROW_PIN + 3] = "<ledrow.3", //
		[IRQ_LEDROW_PIN + 4] = "<ledrow.4", //
		[IRQ_LEDROW_PIN + 5] = "<ledrow.5", //
		[IRQ_LEDROW_PIN + 6] = "<ledrow.6", //
		[IRQ_LEDROW_PIN + 7] = "<ledrow.7", //
		};

void ledrow_core_init(struct avr_t *avr, struct ledrow_t * b, int size)
{
	memset(b, 0, sizeof(*b));
	int i;
	b->avr = avr;

	/*
	 * Register callbacks on all our IRQs
	 */
	b->irq = avr_alloc_irq(&avr->irq_pool, 0, size, irq_names);

	for (int i = 0; i < size; i++)
	{
		avr_irq_register_notify(b->irq + i, ledrow_pin_changed_hook, b);
	}
}

