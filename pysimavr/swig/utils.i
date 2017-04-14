%module(directors="1") utils
%include "constraints.i"


%{
#include "TimerCallback.h"
#include "LoggerCallback.h"

%}


// Enable cross-language polymorphism in the SWIG wrapper. 
%feature("director") TimerCallback;
%feature("director") LoggerCallback;

//avr_cycle_count_t => uint64_t
%apply unsigned long long { avr_cycle_count_t }
%apply unsigned long { uint32_t }
%apply Pointer NONNULL { avr_t* };

%ignore instance; //LoggerCallback* LoggerCallback::instance 

%include "TimerCallback.h"
%include "LoggerCallback.h"