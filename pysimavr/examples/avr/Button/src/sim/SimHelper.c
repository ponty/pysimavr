/*
 * Helper methods for simavr
 *
 *  Created on: Feb 14, 2017
 *      Author: premik
 */

#include "avr_mcu_section.h"


#include <avr/io.h>
#include <stdio.h>

//Embdedde the mcu type and frequency to the elf so simavr can detect it automatically.
//AVR_MCU(F_CPU, "attiny4313");
AVR_MCU(F_CPU, "atmega2560");

//Configure simavr to use an unused register for console output.
AVR_MCU_SIMAVR_CONSOLE(&GPIOR0);

void prnt(const char* msg) {
	for (const char * t = msg; *t; t++)
		GPIOR0 = *t;
}

void dPrint(const char* msg) {
	prnt(msg);
	prnt("\r");
}

void dPrintNum(const char* msg, int16_t num) {
	prnt(msg);
	prnt(" ");

	char buffer[8];
	snprintf(buffer, sizeof(buffer), "%d", num);
	dPrint(buffer);

}

