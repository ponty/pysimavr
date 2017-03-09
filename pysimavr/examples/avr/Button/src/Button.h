/*
 * Software only button. Based on a simple state machine. Button changes its state and emits events on some transitions.
 * The recognizeStateAndEvent method needs to be called periodically.
 *
 *  Created on: Oct 21, 2015
 *      Author: premik
 */

#ifndef BUTTON_H_
#define BUTTON_H_

#include <stdint.h>

#define BT_DEBOUNCE_TIMEOUT 3
#define BT_KEEPING_HOLDING_TIMEOUT 6
#define BT_KEEPING_HOLDING_CHECK_SKIPS 40

enum {
	BT_STATUS_KEEPING_UP = 0,
	BT_STATUS_UP,
	BT_STATUS_BOUNCING_DOWN,
	BT_STATUS_DOWN,
	BT_STATUS_BOUNCING_UP,
	BT_STATUS_HOLDING_DOWN
};

enum {
	BT_EVENT_NONE = 0,
	BT_EVENT_PRESSED,
	BT_EVENT_HELD,
	BT_EVENT_RELEASED,
	BT_EVENT_HOLDING,
	BT_EVENT_KEPT_UP,
	BT_EVENT_KEEPING_UP
};

/*(STATUS) {EVENT} t=timeout
 *
 *
 *    ╭──╮                       ╭──╮                         ╭──╮
 *    0  │                      1,0 │                         1  │
 *    │  ▼                       │  ▼                         │  ▼
 *   (UP)—1—{PRESSED}──┬───—▶ (BOUNCING_DOWN)——t————————————▶ (DOWN)
 *    │               ╱                                    ___╱0   │t {HELD}
 *    t              ╱                                    ▼        ▼
 *    │{KEPT_UP}    ╱   (UP)◀——t——(BOUNCING_UP)◀⟵——{RELEASED}——0—(HOLDING_DOWN)
 *    ▼            ╱              │  ▲                           │  ▲   │  ▲
 * (KEEPING_UP)_1_╱              1,0 │                           1  │   t  │
 *   │  ▲                         ╰──╯                           ╰──╯   ╰──╯{HOLDING}
 *   0  │
 *   ╰──╯
 */

typedef struct ButtonStatusStruct {
	uint8_t lastValue :1;
	uint8_t counter :4;
	uint8_t status :3;
} ButtonStatus;

class Button {
private:
	ButtonStatus button;
	void changeStatus(const uint8_t newStatus);

public:
	Button();
	uint8_t recognizeStateAndEvent(const uint8_t val, const uint16_t gcounter);

};

#endif /* BUTTON_H_ */
