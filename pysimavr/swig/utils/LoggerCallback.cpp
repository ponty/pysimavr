/*
 * LoggerCallback.cpp
 *
 *  Created on: Mar 17, 2017
 *      Author: premik
 */

#include "LoggerCallback.h"
#include "sim_avr.h"
#include <stdio.h>
#include <stdexcept>

LoggerCallback* LoggerCallback::instance = NULL;


static void _logger_callback(avr_t* avr, const int level, const char * format, va_list args) {
	LoggerCallback* inst = LoggerCallback::instance;
	if (inst == NULL) {
		return;
	}

	char buff[256];
	int size;
	size = vsnprintf(buff, sizeof(buff), format, args);
	if (size <= 0) {
		return;
	}
	inst->on_log(buff, level);
}

LoggerCallback::LoggerCallback() {
	if (instance != NULL) {
			delete instance;
	}
	instance = this;
	avr_global_logger_set(_logger_callback);
}

LoggerCallback::~LoggerCallback() {
	instance = NULL;
	avr_global_logger_set(NULL);//This resets simavr logger to the default one
}

void LoggerCallback::on_log(const char* msg, const int level) {
	//When used a pure virtual somehow it is not possible to init the class from python.
	//As the swig wrapper still thinks the class is abstract despite it was extended from python. 
	throw std::runtime_error("Virtual method on_logger is not implemented.");
	//std::cout << "Not implemented" << std::endl;
}
