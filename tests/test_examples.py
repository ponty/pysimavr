from easyprocess import EasyProcess
from nose.tools import eq_
from pysimavr.examples import vcd, hello, simple
# import tempfile


vcd
hello
simple

def test_vcd():
#     vcdfile = tempfile.mkdtemp() + '/delay.vcd'
    eq_(0, EasyProcess('python -m pysimavr.examples.vcd').call().return_code)


def test_hello():
    eq_(0, EasyProcess('python -m pysimavr.examples.hello').call().return_code)


def test_simple():
    eq_(0, EasyProcess('python -m pysimavr.examples.simple').call().return_code)
