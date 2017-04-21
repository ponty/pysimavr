from path import Path
from pysimavr.proxy import Proxy
from pysimavr.logger import init_simavr_logger, get_simavr_logger
from pysimavr.swig.simavr import elf_firmware_t, elf_read_firmware


class Firmware(Proxy):
    _reserved = 'mcu filename read'.split()

    def __init__(self, filename=None):
        if get_simavr_logger() is None:
            init_simavr_logger()
        self.filename = None
        self.backend = elf_firmware_t()
        if filename:
            self.read(filename)

    def read(self, filename):
        filename = Path(filename).abspath()
        ret = elf_read_firmware(str(filename), self.backend)
        if ret == -1:
            raise ValueError(filename + ' could not be loaded!')
        self.filename = filename

    @property
    def mcu(self):
        return self.mmcu

    @mcu.setter
    def mcu(self, value):
        self.mmcu = value
