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



update simavr sources
======================


copy::

    $SIMAVR/include         ->   $PYSIMAVR/pysimavr/swig/include
    $SIMAVR/simavr/cores    ->   $PYSIMAVR/pysimavr/swig/cores
    $SIMAVR/simavr/sim      ->   $PYSIMAVR/pysimavr/swig/sim

    $AVR_LIBC_INCLUDE/avr   ->   $PYSIMAVR/pysimavr/swig/include/avr
    
    (Ubuntu: /usr/lib/avr/include/avr/)
    
    
   