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


f_cpu=16000000
fps=20
speed=1
timespan=5

if __name__ == "__main__":
    ArduinoSim(snippet=snippet,
           timespan=timespan,
           serial_line_logger=logger,
           f_cpu=f_cpu,
           fps=fps,
           speed=speed,
           ).run()
