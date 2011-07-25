#ifndef __LEDROW_CORE_H__
#define __LEDROW_CORE_H__

#include "sim_irq.h"

enum
{
	IRQ_LEDROW_PIN,
//	LEDROW_PIN_COUNT,
};
#define LEDROW_MAX_PIN_COUNT 64

typedef struct ledrow_t
{
	avr_irq_t * irq;
	struct avr_t * avr;

	uint64_t pinstate;
	uint64_t pinstate_changed;

} ledrow_t;

void ledrow_core_init(struct avr_t *avr, struct ledrow_t * b, int size);


#endif 
