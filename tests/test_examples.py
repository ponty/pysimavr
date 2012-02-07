from pysimavr.examples import vcd, hello, simple
import tempfile

def test_vcd():
    vcdfile= tempfile.mkdtemp() + '/delay.vcd'
#    vcdfile='delay.vcd'
    vcd.run_sim(vcdfile=vcdfile)
    
    
def test_hello():
    hello.run_sim()    
    
    
def test_simple():
    simple.run_sim()    
    
    
    
    
    
    
    
    
    
