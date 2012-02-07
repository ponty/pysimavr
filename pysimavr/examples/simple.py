from pysimavr.avr import Avr
from entrypoint2 import entrypoint

@entrypoint
def run_sim():
    avr=Avr(mcu='atmega48',f_cpu=8000000)
    avr.step(1)
    print avr.pc
