pysimavr is a python wrapper for simavr_ which is AVR_ and arduino_ simulator

Links:
 * home: https://github.com/ponty/pysimavr
 * documentation: http://pysimavr.readthedocs.org
 * PYPI: https://pypi.python.org/pypi/pysimavr

|Travis| |Coveralls| |Latest Version| |Supported Python versions| |License| |Downloads| |Code Health| |Documentation|
 
Features:
 - python wrapper using swig_
 - simavr_ source code is included for easier installation
 - object oriented interface on top of the generated interface
 - maximum speed can be real-time
 - serial communication
 - check simavr_ documentation
 
Known problems:
 - included simavr_ source code is not up to date
 - Python 3 is not supported
 - tested only on linux
 - more tests needed
 - PWM simulation is not real-time
 - missing PWM modes
 - a lot of messages on stdout
 - LCD simulator is not fully implemented

Possible usage:
 - unit test
 - simulator
 
Similar projects:
 - simavr_
 - `emulino <http://hewgill.com/journal/entries/507-emulino-arduino-cpu-emulator>`_ 
 - `Arduino Unit <http://code.google.com/p/arduinounit/>`_
 - `arduemu <http://radpartbrainmat.blogspot.com/search/label/arduemu>`_
 
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

ignore these in simavr_ doc:
 - OpenGl (freeglut)
 - gcc-avr
 - avr-libc
 - make
 
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
    # optional for examples:
    sudo pip install entrypoint2
    # optional for some tests:
    sudo apt-get install freeglut3-dev scons

Uninstall
---------

::

    # as root
    pip uninstall pysimavr


.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: https://pypi.python.org/pypi/pip
.. _arduino: http://arduino.cc/
.. _python: http://www.python.org/
.. _simavr: https://github.com/buserror/simavr
.. _swig: http://www.swig.org/
.. _avr: http://en.wikipedia.org/wiki/Atmel_AVR

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
