#ifndef __BOARD_CORE_H__
#define __BOARD_CORE_H__

#include "sim_irq.h"

#define MAX_DIGITS 100
#define MAX_PINS (SEGMENT_PINS+MAX_DIGITS)

enum
{
	IRQ_SGM7_A, //segment a
	IRQ_SGM7_B,
	IRQ_SGM7_C,
	IRQ_SGM7_D,
	IRQ_SGM7_E,
	IRQ_SGM7_F,
	IRQ_SGM7_G,
	IRQ_SGM7_P, // point
	IRQ_DIG0,
};

//    ---A---
//    |     |
//    F     B
//    |     |
//    ---G---
//    |     |
//    E     C
//    |     |
//    ---D---   P

#define SEGMENT_PINS  8

#define SEGMENT_A   (1<<0)
#define SEGMENT_B   (1<<1)
#define SEGMENT_C   (1<<2)
#define SEGMENT_D   (1<<3)
#define SEGMENT_E   (1<<4)
#define SEGMENT_F   (1<<5)
#define SEGMENT_G   (1<<6)
#define SEGMENT_P   (1<<7)

typedef uint64_t pinstate_t;
typedef uint8_t digit_t;

typedef struct sgm7_t
{
	avr_irq_t * irq;
	struct avr_t * avr;

	pinstate_t pinstate; // 'actual' data pins (IRQ bit field)
	int digit_count; // visibles characters
	digit_t digit_segments[MAX_DIGITS]; //segments in 8 bit
	digit_t digit_segments_changed[MAX_DIGITS]; //segments in 8 bit

	//	digit_t digits_aggregate[MAX_DIGITS]; //
	//	digit_t digits_fadeout[MAX_DIGITS]; //segments in 8 bit
	//	float fadeout; // sec

	int digit_pin[MAX_DIGITS];
	//	int digit_inverted[MAX_DIGITS];
	char digit_port[MAX_DIGITS];

	int segment_pin[SEGMENT_PINS];
	//	int segment_inverted[SEGMENT_PINS];
	char segment_port[SEGMENT_PINS];

	//int pin_invert[MAX_PINS];
} sgm7_t;

void sgm7_core_init(struct avr_t *avr, struct sgm7_t * b, int digit_count);
//void sgm7_core_dump(struct sgm7_t * b);
//void sgm7_core_invert_pin(struct sgm7_t * b, int index);
digit_t sgm7_get_digit_segments(struct sgm7_t * b, int index);
digit_t sgm7_reset_dirty(struct sgm7_t * b, int index);

#endif 
