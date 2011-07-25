from swig.simavr import avr_connect_irq
import logging
import operator

log = logging.getLogger(__name__)

def connect_irqs(irq_out, irq_in, bidirectional=False):
    avr_connect_irq(irq_out, irq_in)
    if bidirectional:
        avr_connect_irq(irq_in, irq_out)

def connect_pins_by_rule(rule, device_map, vcd=None):
    ''' rule example:
    
    B0 --> D4 -> vcd
    
    B1 <== D5
    B2  => D6
    #B3 <=> D7
    '''
    lines = rule.strip().splitlines()
    
    # remove comments
    lines = [x.split('#')[0] for x in lines] 
    
    # remove empty lines
    lines = [x.strip() for x in lines]
    lines = filter(bool, lines)
    
    # split by '|'
    if len(lines):
        lines = reduce(operator.add, [x.split('|') for x in lines])

    lines = [x.strip().replace('-', '=').replace('==', '=').replace(' ', '') for x in lines]
    
    class _dev(object):
        def __init__(self):
            self.vcd = None
            self.dev = None
            self.devname = None
            self.irq = None
    
    def addsignal(vcd, d):
        name = '%s.%s' % (d.devname, d.irqname)
        vcd.add_signal(d.irq, name=name)
        
    def con(d1, d2):
        if d1.vcd and d2.dev:
            addsignal(d1.vcd, d2)
        elif d2.vcd and d1.dev:
            addsignal(d2.vcd, d1)
        elif d1.dev and d2.dev:
            connect_irqs(d1.irq, d2.irq, bidirectional=False)
            log.debug('connecting %s -> %s' % 
                          ((d1.devname, d1.irqname), (d2.devname, d2.irqname)))
        
    def getdev(s):
        d = _dev()
        if s == 'vcd':
            d.vcd = vcd
        else:
            ls = s.split('.')
            d.devname = ls[0]
            d.irqname = ls[1]
            d.dev = device_map[ls[0]]  
            if d.dev:        
                d.irq = d.dev.getirq(ls[1])
        return d
    
    def process(x):
        if '<=>' in x:            
            toleft = 1
            toright = 1
        elif '<=' in x:            
            toleft = 1
            toright = 0
        elif '=>' in x:            
            toleft = 0
            toright = 1
        else:            
            toleft = 1
            toright = 1
        x = x.replace('>', '')
        x = x.replace('<', '')
        ls = map(getdev, x.split('=')) 
        
        if toright:
            con(ls[0], ls[1])
        if toleft:
            con(ls[1], ls[0])
        
    for x in lines:
        elems = x.split('=')
        pairs = zip(elems[:-1], elems[1:])
        for a, b in pairs:
            process(a + '=' + b)
    
#def connect_pins_by_map(dev1, dev2, rule):
#    ''' rule example:
#    
#    B0 --> D4
#    
#    B1 <== D5
#    B2  => D6
#    #B3 <=> D7
#    '''
#    lines = [x.strip() for x in rule.strip().splitlines()]
#    lines = filter(bool, lines)
#    lines = filter(lambda x: '#' not in x, lines)
#    def con(irq1, irq2):
#        connect_irqs(irq1, irq2, bidirectional=False)
#    for x in lines:
#        x = x.strip().replace('-', '=').replace('==', '=').replace(' ', '')
#        if '<=>' in x:            
#            toleft = 1
#            toright = 1
#        elif '<=' in x:            
#            toleft = 1
#            toright = 0
#        elif '=>' in x:            
#            toleft = 0
#            toright = 1
#        else:            
#            toleft = 1
#            toright = 1
#        x = x.replace('>', '')
#        x = x.replace('<', '')
#        ls = x.split('=') 
#        irq1 = dev1.getirq(ls[0])
#        irq2 = dev2.getirq(ls[1])
#        if toright:
#            log.debug('connecting %s -> %s' % tuple(ls))
#            con(irq1, irq2)
#        if toleft:
#            log.debug('connecting %s -> %s' % tuple(reversed(ls)))
#            con(irq2, irq1)
        
