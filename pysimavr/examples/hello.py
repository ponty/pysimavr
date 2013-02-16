from pysimavr.sim import ArduinoSim
from entrypoint2 import entrypoint


@entrypoint
def run_sim():
    print ArduinoSim(snippet='Serial.println("hello!");').get_serial()
