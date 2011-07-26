from path import path
from pyavrutils.arduino import Arduino
from pysimavr.avr import Avr
from pysimavrgui.examples.sim.arduino import arduino_sim
import csv

TEMPLATE = '''
void setup()
{
    Serial.begin(9600);

    CODE_SNIPPET;
    
}

void loop()
{
}
'''

root = path(__file__).parent.parent.abspath()

def targets():
    return Avr.arduino_targets

def code2cc(code_snippet, mcu):
    cc = Arduino(mcu=mcu, extra_lib=root)
    code = TEMPLATE.replace('CODE_SNIPPET', code_snippet)
    cc.build(code)
    elf = cc.output
    s = arduino_sim(
            mcu=mcu,
#            f_cpu=cc.f_cpu,
#            vcdfile='arduino.vcd',
#            speed=1,
#            fps=20,
            timeout=0.1,
            visible=0,
#            image_file='',
            buttons_enable=0,
            vcd_enable=0,
            spk_enable=0,
            udp_enable=1,
            elf=elf,
            )
    return cc, s

def code2size(code_snippet, mcu):
    cc, s = code2cc(code_snippet, mcu)
    return cc.size()

def code2ser(code_snippet, mcu):
    cc, s = code2cc(code_snippet, mcu)
    return s

def snippet_doc(csvinput, outdir):
    '''generate screenshots from code snippets'''
    d = outdir
    f = open(csvinput, 'rb')
    reader = csv.reader(f)
  
    fx = open(d / 'generated_examples.csv', 'wb')
    writer = csv.writer(fx)
#    info('generating ' + fx.name)
    
    path(d / 'generated_template.c').write_text(TEMPLATE)
    
    writer.writerow([
                     'comment',
                     'snippet',
                     ] + targets())

    for i, (src, comment) in enumerate(reader):
        src = src.replace('{LF}', '\n')        
        fcode = path(d / 'generated_code_' + str(i) + '.c')
#        info('generating ' + fcode)
        fcode.write_text(src)        
        
        outs = []
        for mcu in targets():
#            info('simulating output ' + mcu)
            flog = path(d / 'generated_log_' + mcu + '_' + str(i) + '.c')
            flog.write_text(code2ser(src, mcu))        
            outs += ['.. literalinclude:: ' + flog.name]
        writer.writerow([
                         comment,
                         '.. literalinclude:: ' + fcode.name,
                         ] + outs)


def libsize(csvinput, outdir, mcu='atmega168'):
    '''calculate lib size'''
    d = outdir
    f = open(csvinput, 'rb')
    reader = csv.reader(f)
  
    fx = open(d / 'generated_code_sizes.csv', 'wb')
    writer = csv.writer(fx)
#    info('generating ' + fx.name)
    
#    path(d / 'generated_template.c').write_text(TEMPLATE)
    for i, (src, comment) in enumerate(reader):
        src = src.replace('{LF}', '\n')        
        fcode = d / 'generated_code4size_' + str(i) + '.c'
        path(fcode).write_text(src)
#        info('generating ' + fcode)
        
        size = code2size(src, mcu)   
        empty_size = code2size('', mcu)
           
        writer.writerow([
                         comment,
                         '.. literalinclude:: ' + fcode.name,
                         size.program_bytes - empty_size.program_bytes,
                         size.data_bytes - empty_size.data_bytes,
                         ])

