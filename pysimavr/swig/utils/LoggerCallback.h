/*
 * LoggerCallback.h
 *
 *  Created on: Mar 17, 2017
 *      Author: premik
 */

#ifndef UTILS_LOGGERCALLBACK_H_
#define UTILS_LOGGERCALLBACK_H_

#include "sim_avr_types.h"

/*
 * Propagation of the simavr logs up to a Python logger. There is one global 
 * instance of this class being hold internally since the simavr logging mechanism 
 * doesn't pass an arbitrary (void*)param argument in this case.
 * Therefore the logger is global for all simavr instances.
 */
class LoggerCallback {
public:
	static LoggerCallback* instance;//The (only) one global logger instance
	
	LoggerCallback();
	virtual ~LoggerCallback();	
	virtual void on_log(const char* msg, const int level);//Implement this one in Pyhton class.
};



#endif /* UTILS_LOGGERCALLBACK_H_ */
