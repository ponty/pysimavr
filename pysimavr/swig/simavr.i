 %module simavr
 %{
 /* Includes the header in the wrapper code */
#include "sim_irq.h"
#include "sim_io.h"
#include "sim_avr.h"
#include "avr_ioport.h"
#include "sim_elf.h"
#include "sim_gdb.h"
#include "sim_vcd_file.h"
#include <unistd.h>
#include <pthread.h>

avr_irq_t* get_irq_at(avr_irq_t* irq, int index)
{
	return irq+index;
}
int _pause_thread;
int _steps;
uint64_t _cycles;
avr_t* _avr;
int _terminate;
static void * avr_thread(void * ignore) 
{
	while (!_terminate) 
	{		
//		while (_pause_thread && _steps==0 && _cycles <= _avr->cycle) 
//		{
//			usleep(1000);
//		}

		if (_cycles > _avr->cycle)
		{
			while(_cycles > _avr->cycle)
			{
				avr_run(_avr);
			}
		}
		else if (_steps>0)
		{
			while(_steps>0)
			{
				_steps--;
				avr_run(_avr);
			}
		}
		else if (!_pause_thread)
		{
			avr_run(_avr);
		}
		else
		{
			usleep(1000);
		}
	}
//	printf("Thread done.\n");
	pthread_exit((void*) ignore);
}
pthread_t _thread;
void avr_start_thread(avr_t* avr)
{
	_terminate=0;
	_pause_thread=1;
	_steps=0;
	_cycles=0;
	_avr=avr;	
//	pthread_t run;
	int rc=pthread_create(&_thread, NULL, avr_thread, NULL);
    if (rc)
    {
       printf("ERROR; return code from pthread_create() is %d\n", rc);
       exit(-1);
    }
}
void avr_terminate_thread()
{
	_terminate=1;
	pthread_join(_thread, NULL);
}

void avr_pause_thread()
{
	_pause_thread=1;	
}
void avr_continue_thread()
{
	_pause_thread=0;	
}
void avr_step_thread(int steps)
{
	_steps=steps;	
}
uint8_t avr_fpeek(avr_t* avr, int addr)
{
	return avr->flash[addr];
}
uint8_t avr_peek(avr_t* avr, int addr)
{
	return avr->data[addr];
}

//void avr_thread_step_cycles(avr_t* avr, uint64_t cycles)
//{
//	_cycles = avr->cycle + cycles;
//}

void avr_thread_goto_cycle(avr_t* avr, uint64_t cycles)
{
	_cycles = cycles;
}

%}
%ignore AVR_IOCTL_IOPORT_GETIRQ_REGBIT;    

long AVR_IOCTL_IOPORT_GETIRQ(char _name)
{
	return AVR_IOCTL_DEF('i','o','g',(_name));
}


%apply unsigned long { uint32_t }
%apply unsigned long long { uint64_t }
%apply unsigned char { uint8_t }
%apply unsigned short { uint16_t }
// %apply unsigned int { avr_irq_t }

 /* Parse the header file to generate wrappers */
%include "sim_irq.h"
%include "sim_io.h"
%include "sim_avr.h"
%include "avr_ioport.h"
%include "sim_elf.h"
%include "sim_gdb.h"
%include "sim_vcd_file.h"


extern void avr_step_thread(int steps);
extern void avr_pause_thread();
extern void avr_continue_thread();
extern void avr_start_thread(avr_t* avr);
extern uint8_t avr_fpeek(avr_t* avr, int addr);
extern uint8_t avr_peek(avr_t* avr, int addr);
extern avr_irq_t* get_irq_at(avr_irq_t* irq, int index);
//extern void avr_thread_step_cycles(avr_t* avr, uint64_t cycles);
extern void avr_thread_goto_cycle(avr_t* avr, uint64_t cycles);
extern void avr_terminate_thread();
