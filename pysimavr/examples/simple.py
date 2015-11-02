from pysimavr.avr import Avr

if __name__ == "__main__":
    avr = Avr(mcu='atmega48', f_cpu=8000000)
    print( avr.pc )
    avr.step(1)
    print( avr.pc )
    avr.step(1)
    print( avr.pc )
    
    avr.terminate()