#include "simavr_logger.h"
#include <stdio.h>
#include <stdarg.h>
#include "sim_avr.h"
#include "avr_uart.h"

static char buff[256];
static int size = -1;
static int lastLevel = 0;

const char* mem_logger_read_line()
{
	if (size < 0 || size > sizeof(buff)) {
		return NULL;
	}
	size = -1;
	return buff;
}

int mem_logger_last_log_level() {
	return lastLevel;
}


void mem_logger_print(avr_t* avr, const int level, const char * format,
		va_list args)
{
	// Notice that only when this returned value is non-negative and less than n, the string has been completely written.
	size = vsnprintf(buff, sizeof(buff), format, args);
	lastLevel = level;
}

void use_mem_logger()
{
	avr_global_logger_set(mem_logger_print);
}

