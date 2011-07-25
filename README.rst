pysimavr is a python wrapper for simavr_

Links:
 * home: https://github.com/ponty/pysimavr
 * documentation: http://ponty.github.com/pysimavr
 
Features:
 - python wrapper using swig_
 - object oriented interface on top of the generated interface
 - maximum speed can be real-time

Known problems:
 - Python 3 is not supported
 - tested only on linux
 
Basic usage
============

    >>> from pysimavr.avr import Avr
    >>> avr=Avr(mcu='atmega48',f_cpu=8000000)
    >>> firmware = Firmware('lcd.elf')
    >>> avr.load_firmware(firmware)


Installation
============

check simavr_ doc: http://gitorious.org/simavr/pages/GetStarted

ignore these in simavr_ doc:
 - OpenGl (freeglut)
 - gcc-avr
 - avr-libc
 - make
 
General
--------

 * install python_
 * install setuptools_
 * install swig_ (for source build only)
 * install header files and a static library for Python  (for source build only)
 * install a compiler  (for source build only)
 * install elf library 
 * install the program::

    # as root
    easy_install pysimavr


Ubuntu
----------
::

    sudo apt-get install python-setuptools
    sudo apt-get install swig
    sudo apt-get install python-dev
    sudo apt-get install gcc
    sudo apt-get install libelf-dev
    sudo easy_install pysimavr

Uninstall
----------

first install pip_::

    # as root
    pip uninstall pysimavr


.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: http://pip.openplans.org/
.. _arduino: http://arduino.cc/
.. _python: http://www.python.org/
.. _simavr: http://gitorious.org/simavr
.. _swig: http://www.swig.org/


