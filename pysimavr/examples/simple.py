from pysimavr.avr import Avr

avr=Avr(mcu='atmega48',f_cpu=8000000)
avr.step(1)
print avr.pc
