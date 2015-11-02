from pysimavr.sim import ArduinoSim


vcdfile='delay.vcd'
snippet = '''
    Serial.println("start");
    pinMode(0, OUTPUT);
    digitalWrite(0, HIGH);
    delay(100);
    digitalWrite(0, LOW);
    delay(100);
    digitalWrite(0, HIGH);
    delay(100);
    digitalWrite(0, LOW);
    delay(100);
    Serial.println("end");
'''

if __name__ == "__main__":
    sim = ArduinoSim(snippet=snippet, vcd=vcdfile, timespan=0.5)
    sim.run()
