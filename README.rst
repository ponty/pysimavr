pysimavr is a python wrapper for simavr_ which is AVR_ and arduino_ simulator

Links:
 * home: https://github.com/ponty/pysimavr
 * documentation: http://pysimavr.readthedocs.org
 * PYPI: https://pypi.python.org/pypi/pysimavr

|Travis| |Coveralls| |Latest Version| |Supported Python versions| |License| |Downloads| |Code Health| |Documentation|
 
Features:
 - python wrapper using swig_
 - simavr_ source code and avr-libc_ headers are included for easier installation
 - object oriented interface on top of the generated interface
 - maximum speed can be real-time
 - serial communication
 - check simavr_ documentation
 
Basic usage
===========

    >>> from pysimavr.avr import Avr
    >>> avr=Avr(mcu='atmega48',f_cpu=8000000)
    >>> firmware = Firmware('lcd.elf')
    >>> avr.load_firmware(firmware)

    
    >>> from pysimavr.sim import ArduinoSim
    >>> print ArduinoSim(snippet='Serial.print("hello!");').get_serial()
    hello!

Installation
============

check simavr_ documentation
 
General
-------

 * install python_
 * install pip_
 * install swig_ (for source build only)
 * install header files and a static library for Python  (for source build only)
 * install a compiler  (for source build only)
 * install elf library 
 * install the program::

    # as root
    pip install pysimavr


Ubuntu 14.04
------------
::

    sudo apt-get install python-pip
    sudo apt-get install swig python-dev gcc libelf-dev arduino
    sudo pip install pysimavr
    # optional for some tests:
    sudo apt-get install freeglut3-dev scons

Uninstall
---------

::

    # as root
    pip uninstall pysimavr

Usage
=====

pysimavr.examples.simple::
    
  #-- include('examples/simple.py')--#
  from pysimavr.avr import Avr

  if __name__ == "__main__":
      avr = Avr(mcu='atmega48', f_cpu=8000000)
      print( avr.pc )
      avr.step(1)
      print( avr.pc )
      avr.step(1)
      print( avr.pc )
      
      avr.terminate()
  #-#

Output::

  #-- sh('python -m pysimavr.examples.simple ')--#
  0
  2
  4
  #-#

pysimavr.examples.hello::
    
  #-- include('examples/hello.py')--#
  from pysimavr.sim import ArduinoSim

  if __name__ == "__main__":
      s= ArduinoSim(snippet='Serial.println("hello!");').get_serial()
      print(s)
  #-#

Output::

  #-- sh('python -m pysimavr.examples.hello ')--#
  hello!

  #-#

pysimavr.examples.delay::
    
  #-- include('examples/delay.py')--#
  from pysimavr.sim import ArduinoSim
  import time

  snippet = '''
  int i=0;
  while (1)
  {
      Serial.println(i++);
      _delay_ms(1000);
  }
  '''
  t0 = None


  def logger(x):
      global t0
      t = time.time()
      if not t0:
          t0 = t
      print t - t0, x


  f_cpu=16000000
  fps=20
  speed=1
  timespan=5

  if __name__ == "__main__":
      ArduinoSim(snippet=snippet,
             timespan=timespan,
             serial_line_logger=logger,
             f_cpu=f_cpu,
             fps=fps,
             speed=speed,
             ).run()
  #-#

Output::

  #-- sh('python -m pysimavr.examples.delay ')--#
  0.0 0

  1.00977802277 1

  2.01976013184 2

  3.02968215942 3

  4.03792500496 4

  #-#

vcd export example
------------------

pysimavr.examples.vcd::

  #-- include('examples/vcd.py')--#
  from pysimavr.sim import ArduinoSim


  vcdfile='delay.vcd'
  snippet = '''
      Serial.println("start");
      pinMode(0, OUTPUT);
      digitalWrite(0, HIGH);
      delay(100);
      digitalWrite(0, LOW);
      delay(100);
      digitalWrite(0, HIGH);
      delay(100);
      digitalWrite(0, LOW);
      delay(100);
      Serial.println("end");
  '''

  if __name__ == "__main__":
      sim = ArduinoSim(snippet=snippet, vcd=vcdfile, timespan=0.5)
      sim.run()
  #-#

.. image:: gtkwave_id0.png

File hierarchy
==============

::
  
   |-docs                   sphinx documentation
   |---.build               generated documentation
   |-pysimavr               main python package, high level classes
   |---examples             examples
   |---swig                 all swig files (simavr and parts)
   |-----include            copy of simavr generated *.h files
   |-------avr              copy from avr-libc
   |-----parts              some electronic parts in c
   |-----simavr             simavr as git submodule
   |-tests                  unit tests



How to update external sources
==============================

1. copy avr-libc_ headers   (Ubuntu folder: /usr/lib/avr/include/avr/) into pysimavr/swig/include/avr
2. simavr_ is a git submodule. Run 'make' inside simavr directory, 
   then copy generated sim_core_config.h and sim_core_decl.h into pysimavr/swig/include 
         
            


.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: https://pypi.python.org/pypi/pip
.. _arduino: http://arduino.cc/
.. _python: http://www.python.org/
.. _simavr: https://github.com/buserror/simavr
.. _swig: http://www.swig.org/
.. _avr: http://en.wikipedia.org/wiki/Atmel_AVR
.. _avr-libc: http://www.nongnu.org/avr-libc/

.. |Travis| image:: http://img.shields.io/travis/ponty/pysimavr.svg
   :target: https://travis-ci.org/ponty/pysimavr/
.. |Coveralls| image:: http://img.shields.io/coveralls/ponty/pysimavr/master.svg
   :target: https://coveralls.io/r/ponty/pysimavr/
.. |Latest Version| image:: https://img.shields.io/pypi/v/pysimavr.svg
   :target: https://pypi.python.org/pypi/pysimavr/
.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/pysimavr.svg
   :target: https://pypi.python.org/pypi/pysimavr/
.. |License| image:: https://img.shields.io/pypi/l/pysimavr.svg
   :target: https://pypi.python.org/pypi/pysimavr/
.. |Downloads| image:: https://img.shields.io/pypi/dm/pysimavr.svg
   :target: https://pypi.python.org/pypi/pysimavr/
.. |Code Health| image:: https://landscape.io/github/ponty/pysimavr/master/landscape.svg?style=flat
   :target: https://landscape.io/github/ponty/pysimavr/master
.. |Documentation| image:: https://readthedocs.org/projects/pysimavr/badge/?version=latest
   :target: http://pysimavr.readthedocs.org
