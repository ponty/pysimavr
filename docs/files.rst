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

1. simavr is a git submodule   
2. download avr-libc sources   (Ubuntu folder: /usr/lib/avr/include/avr/)
3. download pysimavr sources    
4. copy over files::

    $AVR_LIBC_INCLUDE/avr   ->   $PYSIMAVR/pysimavr/swig/include/avr
            
5. install pysimavr::
    
    cd $PYSIMAVR
    pip install .
    
    
 
 
 
 
 