import pyvisa
import numpy as np
from time import sleep
import pyvisa
from time import sleep

class Agilent_33220A:
    def __init__(self, address):
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(address)

    def set_offset(self, val):
        self.instrument.write(f'VOLT:OFFS {val}')

    def close(self):
        self.instrument.close()

device = GPIBDevice('GPIB0::30::INSTR')
device.set_offset(1.0)  # Set offset to 1.0 volts
device.close()
