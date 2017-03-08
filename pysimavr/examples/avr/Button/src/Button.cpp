/*
 *  Created on: Oct 21, 2015
 *      Author: premik
 */
#include "Button.h"

#include <string.h>

Button::Button() {
	memset(&button, 0, sizeof(ButtonStatus));
}
void Button::changeStatus(const uint8_t newStatus) {
	button.counter = 0;
	button.status = newStatus;
}

uint8_t Button::recognizeStateAndEvent(const uint8_t val, const uint16_t gcounter) {
	const uint8_t lastValue = button.lastValue;
	button.lastValue = val;

	if (button.status == BT_STATUS_UP) {
		if (val == 1) {
			changeStatus(BT_STATUS_BOUNCING_DOWN);
			return BT_EVENT_PRESSED;
		}
		//val = 0
		if (gcounter % BT_KEEPING_HOLDING_CHECK_SKIPS == 0) {
			button.counter++;
		}
		if (button.counter >= BT_KEEPING_HOLDING_TIMEOUT) {
			changeStatus (BT_STATUS_KEEPING_UP);
			return BT_EVENT_KEPT_UP;
		}
	}

	if (button.status == BT_STATUS_KEEPING_UP) {
		if (val == 1) {
			changeStatus(BT_STATUS_BOUNCING_DOWN);
			return BT_EVENT_PRESSED;
		}
		//val 0 and TO stays in KEEPING_UP
		return BT_EVENT_NONE;
	}

	if (button.status == BT_STATUS_BOUNCING_DOWN || button.status == BT_STATUS_BOUNCING_UP) {
		if (val == lastValue) {
			//Count for how log the value is stable
			button.counter++;
		} else {
			//Changed, reset counter
			button.counter = 0;
		}

		if (button.counter >= BT_DEBOUNCE_TIMEOUT) {
			if (button.status == BT_STATUS_BOUNCING_DOWN) {
				changeStatus(BT_STATUS_DOWN);
			} else {
				changeStatus(BT_STATUS_UP);
			}
		}
	}

	if (button.status == BT_STATUS_DOWN) {
		if (val == 0) {
			changeStatus(BT_STATUS_BOUNCING_UP);
			return BT_EVENT_RELEASED;
		}
		//val = 1
		if (gcounter % BT_KEEPING_HOLDING_CHECK_SKIPS == 0) {
			button.counter++;
		}
		if (button.counter >= BT_KEEPING_HOLDING_TIMEOUT) {
			changeStatus (BT_STATUS_HOLDING_DOWN);
			return BT_EVENT_HELD;
		}
	}

	if (button.status == BT_STATUS_HOLDING_DOWN) {
		if (gcounter % BT_KEEPING_HOLDING_CHECK_SKIPS == 0) {
			button.counter++;
		};
		if (button.counter >= BT_KEEPING_HOLDING_TIMEOUT) {
			//Keep pushing holding event periodically
			button.counter = 0;
			return BT_EVENT_HOLDING;
		}
		if (val == 0) {
			changeStatus(BT_STATUS_BOUNCING_UP);
			return BT_EVENT_RELEASED;
		}
	}

	return BT_EVENT_NONE;

}

