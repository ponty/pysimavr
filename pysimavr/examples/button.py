import pysimavr.connect
from pysimavr.avr import Avr
from pysimavr.firmware import Firmware
from pysimavr.button import Button
from pysimavr.swig.simavr import avr_gdb_init, cpu_Done, cpu_Crashed, cpu_Stopped 
import time
import logging
from os import path

if __name__ == '__main__':   
    print("Start")
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
        
    # Load firmware from ./avr/Button/Debug/Button.elf
    modulePath = path.dirname(path.realpath(__file__))
    fw = Firmware(path.join(modulePath, "avr", "Button", "Debug", "Button.elf"))    
    # fw = Firmware(path.join(modulePath, "avr", "Button", "Release", "Button.elf")
    print("Loading {}".format(fw.filename))
    
    avr = Avr(firmware=fw)  # The Button.elf has mcu and freq info embedded
    # avr = Avr(firmware=fw, mcu='atmega2560', f_cpu=8000000)
    # avr = Avr(firmware=fw, mcu='attiny2313', f_cpu=8000000)  
          
    print("Fw loaded")
    
    # Set the GDB port and start simavr GDB
    avr.gdb_port = 1234;
    avr_gdb_init(avr.backend)
    # avr.state = cpu_Stopped #To let simavr wait on the first instruction for GDB to connect. 
    
    # Get the AVR A3 input pin.
    A3IRQ = avr.getirq(('A', 3));
    
    # Create simavr inbuilt button part.
    b = Button(avr); 
    
    # Get the button's output port and attach it to the AVR input.
    pysimavr.connect.avr_connect_irq(b.getirq(0), A3IRQ)
    
    prevState = -1
    i = 0
 
    # Main loop. 
    try:
        while True:
        
            # Do multiple simavr simulation steps synchronously. 
            # Alternatively inbuilt pysimavr background execution thread can be used.
            avr.step(1000);
            time.sleep(0.01)
            
            # Print any simavr mcu state change.
            if avr.state != prevState:
                prevState = avr.state               
                print("Avr state: {}".format(avr.states[avr.state]));
                
                # Simavr got to a final state. Terminate the main loop since it can't proceed any further.
                if avr.state in (cpu_Done, cpu_Crashed): break; 
                
            i += 1
            
            # Simulate button press once in a while.
            if i % 200 == 50:
                print("Press")                
                b.press(10000);  # Press with autorelease
            
            # if i % 100 == 0:b.up();
            # if i % 100 == 50:b.down();
    
    finally: avr.terminate()   
    print("end")
