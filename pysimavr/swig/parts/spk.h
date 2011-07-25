#ifndef __SPK_CORE_H__
#define __SPK_CORE_H__

#include "sim_irq.h"
#include "sim_avr.h"

#define BUFFER_SIZE  1024
//#define FREQ_SCALE  1000
#define HIGH_VALUE  100
#define LOW_VALUE   1

enum
{
	IRQ_SPK_IN,
	SPK_PIN_COUNT,
};

typedef struct spk_t
{
	avr_irq_t * irq;
	struct avr_t * avr;

	//uint64_t pinstate;
	//uint64_t pinstate_changed;
	char buffer[BUFFER_SIZE];
	char last_value;
	int overrun;
	avr_cycle_count_t start_cycle;
	int freq_scale;

} spk_t;

void spk_core_init(struct avr_t *avr, struct spk_t * b, int rate, float speed);
void spk_reset(struct spk_t * b);
char* spk_read(struct spk_t * b);
int spk_buffer_ready(struct spk_t * b);


#endif 
