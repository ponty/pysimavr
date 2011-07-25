#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "sim_cycle_timers.h"
#include "sgm7.h"
#include "avr_ioport.h"
#include "sim_vcd_file.h"

#define MAX(a,b)         ((a < b) ?  (b) : (a))

//static avr_cycle_count_t refresh_timer(avr_t * avr, avr_cycle_count_t when,
//		void * param)
//{
//	sgm7_t * b = (sgm7_t *) param;
//	for (int i = 0; i < b->digit_count; i++)
//	{
//		b->digits_fadeout[i] = b->digits_aggregate[i];
//		b->digits_aggregate[i] = 0;
//	}
//	return when + avr_usec_to_cycles(avr, (int) (b->fadeout * 1000000));
//}

void calculate_digits(pinstate_t pinstate, digit_t * digits,
		digit_t * digits_changed, int digit_count)
{
	for (int i = 0; i < digit_count; i++)
	{
		digit_t segments = 0;
		if (pinstate & (1 << (IRQ_DIG0 + i)))
		{
			segments = 0;
		}
		else
		{
			if (pinstate & (1 << (IRQ_SGM7_A + 0)))
			{
				segments |= (1 << 0);
			}
			if (pinstate & (1 << (IRQ_SGM7_A + 1)))
			{
				segments |= (1 << 1);
			}
			if (pinstate & (1 << (IRQ_SGM7_A + 2)))
			{
				segments |= (1 << 2);
			}
			if (pinstate & (1 << (IRQ_SGM7_A + 3)))
			{
				segments |= (1 << 3);
			}
			if (pinstate & (1 << (IRQ_SGM7_A + 4)))
			{
				segments |= (1 << 4);
			}
			if (pinstate & (1 << (IRQ_SGM7_A + 5)))
			{
				segments |= (1 << 5);
			}
			if (pinstate & (1 << (IRQ_SGM7_A + 6)))
			{
				segments |= (1 << 6);
			}
			if (pinstate & (1 << (IRQ_SGM7_A + 7)))
			{
				segments |= (1 << 7);
			}
		}
		digits_changed[i] |= digits[i] ^ segments;
		digits[i] = segments;
	}
}

static void sgm7_pin_changed_hook(struct avr_irq_t * irq, uint32_t value,
		void *param)
{
	sgm7_t *b = (sgm7_t *) param;

	//if (b->pin_invert[irq->irq])
	//{
	//	value = !value;
	//}
	b->pinstate = (b->pinstate & ~(1 << irq->irq)) | (value << irq->irq);

	calculate_digits(b->pinstate, b->digit_segments, b->digit_segments_changed,
			b->digit_count);
	//	for (int i = 0; i < b->digit_count; i++)
	//	{
	//		b->digits_aggregate[i] |= b->digit_segments[i];
	//	}

}

static const char * irq_names[33] =
{ [IRQ_SGM7_A] = "<sgm7.A",//
		[IRQ_SGM7_B] = "<sgm7.B",//
		[IRQ_SGM7_C] = "<sgm7.C",//
		[IRQ_SGM7_D] = "<sgm7.D",//
		[IRQ_SGM7_E] = "<sgm7.E",//
		[IRQ_SGM7_F] = "<sgm7.F",//
		[IRQ_SGM7_G] = "<sgm7.G",//
		[IRQ_SGM7_P] = "<sgm7.P", //

		};

int sgm7_core_pin_count(struct sgm7_t * b)
{
	return b->digit_count + SEGMENT_PINS;
}

void sgm7_core_init(struct avr_t *avr, struct sgm7_t * b, int digit_count)
{
	memset(b, 0, sizeof(*b));
	b->digit_count = digit_count;

	//	char * hwini = "hw.ini";
	//int i;
	//	b->fadeout = 0.010;//sec
	//	for (i = 0; i < argc; i++)
	//	{
	//		if (strcmp(argv[i], "--hwini") == 0)
	//		{
	//			hwini = argv[i + 1];
	//		}
	//		if (strcmp(argv[i], "--fadeout") == 0)
	//		{
	//			sscanf(argv[i + 1], "%f", &b->fadeout);
	//		}
	//	}
	//	printf("  hwini=%s\n", hwini);
	//	printf("  fadeout=%f sec\n", b->fadeout);

	//	read_ini(b, hwini);

	b->avr = avr;

	/*
	 * Register callbacks on all our IRQs
	 */
	b->irq
			= avr_alloc_irq(&avr->irq_pool, 0, sgm7_core_pin_count(b),
					irq_names);
	for (int i = 0; i < sgm7_core_pin_count(b); i++)
		avr_irq_register_notify(b->irq + i, sgm7_pin_changed_hook, b);

	//	avr_cycle_timer_cancel(b->avr, refresh_timer, b);
	//	avr_cycle_timer_register_usec(b->avr, (int) (b->fadeout * 1000000),
	//			refresh_timer, b);

	//	printf("%duS is %d cycles for your AVR\n", 37,
	//			(int) avr_usec_to_cycles(avr, 37));
	//	printf("%duS is %d cycles for your AVR\n", 1,
	//			(int) avr_usec_to_cycles(avr, 1));

	//	for (i = 0; i < SEGMENT_PINS; i++)
	//	{
	//		avr_connect_irq(
	//				avr_io_getirq(avr, AVR_IOCTL_IOPORT_GETIRQ(b->segment_port[i]),
	//						b->segment_pin[i]), b->irq + IRQ_SGM7_A + i);
	//	}
	//	for (i = 0; i < b->digit_count; i++)
	//	{
	//		avr_connect_irq(
	//				avr_io_getirq(avr, AVR_IOCTL_IOPORT_GETIRQ(b->digit_port[i]),
	//						b->digit_pin[i]), b->irq + IRQ_DIG0 + i);
	//	}
	//	for (i = 0; i < SEGMENT_PINS; i++)
	//	{
	//		b->pin_invert[IRQ_SGM7_A + i] = b->segment_inverted[i];
	//	}
	//	for (i = 0; i < MAX_DIGITS; i++)
	//	{
	//		b->pin_invert[IRQ_DIG0 + i] = b->digit_inverted[i];
	//	}

}

//void sgm7_core_invert_pin(struct sgm7_t * b, int index)
//{
//	b->pin_invert[index] = 1;
//}

digit_t sgm7_get_digit_segments(struct sgm7_t * b, int index)
{
	return b->digit_segments[index];
}

digit_t sgm7_reset_dirty(struct sgm7_t * b, int index)
{
	digit_t x = b->digit_segments_changed[index];
	b->digit_segments_changed[index] = 0;
	return x;
}
