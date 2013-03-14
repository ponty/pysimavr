from pysimavr.ac import Ac
from pysimavr.avr import Avr
from pysimavr.button import Button
from pysimavr.inverter import Inverter
from pysimavr.lcd import Lcd
from pysimavr.ledrow import LedRow
from pysimavr.sgm7 import Sgm7
from pysimavr.spk import Spk
from pysimavr.udp import Udp


def test():
    avr = Avr(mcu='atmega48', f_cpu=8000000)
    Ac(avr)
    Button(avr)
    Inverter(avr)
    LedRow(avr)
    Sgm7(avr)
    Lcd(avr)
    Spk(avr)

    Udp(avr)
