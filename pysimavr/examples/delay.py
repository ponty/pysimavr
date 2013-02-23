from entrypoint2 import entrypoint
from pysimavr.sim import ArduinoSim
import time

snippet = '''
int i=0;
while (1)
{
    Serial.println(i++);
    _delay_ms(1000);
}
'''
t0 = None


def logger(x):
    global t0
    t = time.time()
    if not t0:
        t0 = t
    print t - t0, x


@entrypoint
def run_sim(timespan=5, f_cpu=16000000, speed=1, fps=20):
    ArduinoSim(snippet=snippet,
               timespan=timespan,
               serial_line_logger=logger,
               f_cpu=f_cpu,
               fps=fps,
               speed=speed,
               ).run()
