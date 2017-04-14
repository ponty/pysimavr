 %module sgm7
 %{
 /* Includes the header in the wrapper code */
#include "sgm7.h"

%}
%apply unsigned long { uint32_t }
%apply unsigned long long { uint64_t }
%apply unsigned char { uint8_t }
%apply unsigned short { uint16_t }
 
 /* Parse the header file to generate wrappers */
%include "sgm7.h"
