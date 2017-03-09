AVR Examples
------------

The `pysimavr/examples/avr`_ folder contains AVR C/C++ examples create only to demonstrate pysimavr capabilities. They can be compiled 
by running ``make``  inside the project root. Or using Eclipse CDT_ with AVR-Eclipse_ plugin.

pysimavr.examples.button
------------------------

This example demonstrates: 
 - Loading *elf* firmware file from the related `AVR project <avr/Button>`_.
 - Setting simavr GDB port and starting the inbuilt simavr GDB server. 
 - Creating the simavr *button* part and connecting it with a simavr input pin. 
 - Simple main loop running simavr *step* command.

Running the example:
 In the main loop there is the *button* being pressed every few seconds. After each press it is then released 
 using the auto-release feature. The actual AVR code prints the detected button events via simavr to the console output. 
 Note the console output from the simulated AVR code is prefixed with **“O:”** by simavr.
Output::

    Start
    Fw loaded
    avr_gdb_init listening on port 1234
    CRITICAL:pysimavr.logger:O:Loop started
    Avr state: Running
    Press
    CRITICAL:pysimavr.logger:O:Pressed
    button_auto_release
    CRITICAL:pysimavr.logger:O:Released
    Press
    CRITICAL:pysimavr.logger:O:Pressed
    button_auto_release
    CRITICAL:pysimavr.logger:O:Released

    
.. _CDT: https://eclipse.org/cdt/    
.. _AVR-Eclipse: https://github.com/mnlipp/avr-eclipse-fork
.. _pysimavr/examples/avr: avr
