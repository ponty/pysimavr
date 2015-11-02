from pysimavr.sim import ArduinoSim

if __name__ == "__main__":
    s= ArduinoSim(snippet='Serial.println("hello!");').get_serial()
    print(s)