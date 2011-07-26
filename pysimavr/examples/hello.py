from pysimavr.serial import ArduinoSimSerial

print ArduinoSimSerial(snippet='Serial.print("hello!");').serial()
