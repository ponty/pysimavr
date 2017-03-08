################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/sim/SimHelper.c 

C_DEPS += \
./src/sim/SimHelper.d 

OBJS += \
./src/sim/SimHelper.o 


# Each subdirectory must supply rules for building sources it contributes
src/sim/%.o: ../src/sim/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: AVR Compiler'
	avr-gcc -DF_CPU=8000000UL -UF_CPU -Wall -g3 -gdwarf-2 -O0 -fpack-struct -fshort-enums -ffunction-sections -fdata-sections -std=gnu99 -funsigned-char -funsigned-bitfields -Wl,--section-start=.mmcu=0x910000 -mmcu=atmega2560 -DF_CPU=8000000UL -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


