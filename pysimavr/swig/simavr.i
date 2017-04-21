 %module simavr
 %{
 
 /* Includes the header in the wrapper code */
#include "sim_avr_types.h"
#include "sim_irq.h"
#include "sim_io.h"
#include "sim_avr.h"
#include "avr_ioport.h"
#include "sim_elf.h"
#include "sim_gdb.h"
#include "sim_vcd_file.h"
#include "simavr_thread.h"

%}

// http://www.swig.org/Doc1.3/Typemaps.html#Typemaps_nn39
%typemap(out) uint8_t [ANY] {
  int i;
  $result = PyList_New($1_dim0);
  for (i = 0; i < $1_dim0; i++) {
    PyObject *o = PyInt_FromLong((long) $1[i]);
    PyList_SetItem($result,i,o);
  }
}

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
%include "simavr_thread.h"

 /* Parse the header file to generate wrappers */
%include "sim_avr_types.h"
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


