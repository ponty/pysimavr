#include "simavr_logger.h"
#include <stdio.h>
#include <stdarg.h>
#include "sim_avr.h"
#include "avr_uart.h"

static char buff[256];
static int size = 0;

char* mem_logger_read_line()
{
	// Notice that only when this returned value is non-negative and less than n, the string has been completely written.
	if (size > 0 && size < sizeof(buff))
		; // OK
	else
		buff[0] = 0;

	return buff;
}

void mem_logger_print(avr_t* avr, const int level, const char * format,
		va_list args)
{
	size = vsnprintf(buff, sizeof(buff), format, args);
}

void use_mem_logger()
{
	avr_global_logger_set(mem_logger_print);
}

