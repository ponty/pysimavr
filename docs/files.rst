File hierarchy
==================

::
  
   |-docs                   sphinx documentation
   |---_build               generated documentation
   |-pysimavr               main python package, high level classes
   |---examples             examples
   |---swig                 all swig files (simavr and parts)
   |-----cores              copy from simavr 
   |-----include            copy from simavr
   |-------avr              copy from avr-libc
   |-----parts              some electronic parts in c
   |-----sim                copy from simavr
   |-tests                  unit tests



How to update simavr sources
=============================

 #. download simavr sources   
 #. download avr-libc sources   (Ubuntu folder: /usr/lib/avr/include/avr/)
 #. download pysimavr sources    
 #. copy over files::

    $SIMAVR/include         ->   $PYSIMAVR/pysimavr/swig/include
    $SIMAVR/simavr/cores    ->   $PYSIMAVR/pysimavr/swig/cores
    $SIMAVR/simavr/sim      ->   $PYSIMAVR/pysimavr/swig/sim
    $AVR_LIBC_INCLUDE/avr   ->   $PYSIMAVR/pysimavr/swig/include/avr
    
 #. copy over files::

    $SIMAVR/include         ->   $PYSIMAVR/pysimavr/swig/include
    $SIMAVR/simavr/cores    ->   $PYSIMAVR/pysimavr/swig/cores
    $SIMAVR/simavr/sim      ->   $PYSIMAVR/pysimavr/swig/sim
    $AVR_LIBC_INCLUDE/avr   ->   $PYSIMAVR/pysimavr/swig/include/avr
    
 #. copy over files::

    cd $PYSIMAVR
    easy_install .
    
 #. install pysimavr::
    
    cd $PYSIMAVR
    easy_install .
    # or
    pip install .
    # or
    paver install
    # or
    python setup.py install
    
    
 
 
 
 
 
 
 
 
 
 
 
 