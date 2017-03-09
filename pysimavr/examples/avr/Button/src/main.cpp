#include <avr/io.h>
#include <util/delay.h>
#include "Button.h"

extern "C" {
#include "sim/SimHelper.h"
}

//Button value on PIN A3
#define BUTTON_VAL() (1-((PINA & _BV(PINA3)) >>(PINA3)))

Button button;

void init() {
	//Input with the internal pull up by default for all the A pins
	PORTA = 0xFF; //Pull up	
	button = Button();
}

int main(void) {
	init();
	uint16_t i = 0;
	uint8_t event = BT_EVENT_NONE;
	dPrint("Loop started");
	while (1) {
		_delay_ms(1);
		uint8_t v = BUTTON_VAL();
		//dPrintNum("but:", v);
		event = button.recognizeStateAndEvent(v, i);


		switch (event) {
		case BT_EVENT_PRESSED:
			dPrint("Pressed");
			break;
		case BT_EVENT_RELEASED:
			dPrint("Released");
			break;
		case BT_EVENT_KEPT_UP:
			dPrint("Kept up");
			break;
		case BT_EVENT_HELD:
			dPrint("Held");
			break;
		case BT_EVENT_HOLDING:
			dPrint("Holding");
			break;
		}
		i++;

	}
}
