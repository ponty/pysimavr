Usage
==================

pysimavr.examples.simple:
    
.. literalinclude:: ../pysimavr/examples/simple.py

.. program-output:: python -m pysimavr.examples.simple
    :prompt:

pysimavr.examples.hello:
    
.. literalinclude:: ../pysimavr/examples/hello.py

.. program-output:: python -m pysimavr.examples.hello
    :prompt:

vcd export example
-------------------------

pysimavr.examples.vcd:

.. literalinclude:: ../pysimavr/examples/vcd.py

.. runblock:: pycon

    >>> from pysimavr.examples.vcd import run_sim
    >>> run_sim(vcdfile='docs/vcd.vcd')
    
.. gtkwave:: docs/vcd.vcd
    

unit test example
-------------------------

pysimavr/examples/test_example.py

.. literalinclude:: ../pysimavr/examples/test_example.py

.. program-output:: nosetests --verbose pysimavr/examples/test_example.py
    :prompt:
