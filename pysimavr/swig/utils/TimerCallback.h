/*
 * TimerCallback.h
 *
 *  Created on: Mar 8, 2017
 *      Author: premik
 */

#ifndef UTILS_TIMERCALLBACK_H_
#define UTILS_TIMERCALLBACK_H_

#include "sim_time.h"

/*
 * Bridges simavr Cycle timer functionaly from C to Python via C++.
 *
 * After the TimerCallback is created the set_timer_* method must be called to
 * get the timer started.
 * The set_timer_* methods can be called repeatedly to change the schedule or to start over.
 *
 */
class TimerCallback {
public:
	TimerCallback(struct avr_t* avr);
	virtual ~TimerCallback();
	void set_timer_cycles(avr_cycle_count_t when);
	void set_timer_usec(uint32_t when);
	void cancel();

	/*
	 * Check to see if a timer is present, if so, return the number (+1) of
	 * cycles left for it to fire, and if not present, return zero
	 */
	avr_cycle_count_t status();

	/*
	 * The virtual method which must be implemented in the extendig Python class.
	 * The return value indicates when (mcu cycle) the next callback should occur.
	 * Return 0 to stop.
	 */
	virtual avr_cycle_count_t on_timer(avr_cycle_count_t when);


protected:
	struct avr_t* avr;

};


#endif /* UTILS_TIMERCALLBACK_H_ */
