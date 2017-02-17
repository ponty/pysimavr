#pragma once

#ifdef __cplusplus
extern "C" {
#endif


const char* mem_logger_read_line();
int mem_logger_last_log_level();
//void mem_logger_print(avr_t* avr, const int level, const char * format, ... );
void use_mem_logger();


#ifdef __cplusplus
}
#endif
