#include <stdlib.h>
#include <stdio.h>
#include <string.h>
//#include "sim_cycle_timers.h"
#include "spk.h"
#include "avr_ioport.h"
//#include "sim_vcd_file.h"

void spk_buffer_set(struct spk_t * b, int start, int value)
{
	for (int i = start; i < BUFFER_SIZE; i++)
	{
		b->buffer[i] = value;
	}
}

static void spk_pin_changed_hook(struct avr_irq_t * irq, uint32_t value,
		void *param)
{
	spk_t *b = (spk_t *) param;

	avr_cycle_count_t current_cycle = b->avr->cycle;
	int pos = (current_cycle - b->start_cycle) / b->freq_scale;
	//	printf("current_cycle=%d b->start_cycle=%d pos=%d \n", current_cycle, b->start_cycle, pos);

	//	printf(" current_cycle=%d", current_cycle);
	//	printf(" b->start_cycle=%d", b->start_cycle);
	//	printf(" pos=%d \n", pos);

	b->last_value = value ? HIGH_VALUE : LOW_VALUE;
	if (pos < 0)
	{
		printf("negative pos\n");
		pos = 0;
	}
	if (pos >= BUFFER_SIZE)
	{
		printf("overrun pos=%d\n", pos);
		b->overrun = 1;
		pos = BUFFER_SIZE - 1;
	}

	spk_buffer_set(b, pos, b->last_value);

	//	printf("buffer=%s \n", b->buffer);
	//printf("spk=%d\n", value);

	//b->pinstate = (b->pinstate & ~(1 << irq->irq)) | (value << irq->irq);
	//b->pinstate_changed |= (1 << irq->irq);
}

static const char * irq_names[SPK_PIN_COUNT] =
{ [IRQ_SPK_IN] = "<spk", };

void spk_core_init(struct avr_t *avr, struct spk_t * b, int rate, float speed)
{
	memset(b, 0, sizeof(*b));
	//int i;
	b->avr = avr;

	/*
	 * Register callbacks on all our IRQs
	 */
	b->irq = avr_alloc_irq(&avr->irq_pool, 0, 1, irq_names);
	avr_irq_register_notify(b->irq, spk_pin_changed_hook, b);

	b->freq_scale = (speed * avr->frequency) / rate;
	printf("b->freq_scale=%d \n", b->freq_scale);

	spk_reset(b);
}

int spk_buffer_ready(struct spk_t * b)
{
	avr_cycle_count_t current_cycle = b->avr->cycle;
	int pos = (current_cycle - b->start_cycle) / b->freq_scale;
	return pos > 100;
}

char* spk_read(struct spk_t * b)
{
	avr_cycle_count_t current_cycle = b->avr->cycle;
	int pos = (current_cycle - b->start_cycle) / b->freq_scale;
	b->buffer[pos] = 0;
	return b->buffer;
}

void spk_reset(struct spk_t * b)
{
	spk_buffer_set(b, 0, b->last_value);
	b->start_cycle = b->avr->cycle;
	//	printf("reset b->start_cycle=%d \n",b->start_cycle);
}
