import pyvisa
import numpy as np
from time import sleep
import pyvisa

class Agilent_33220A:
    def __init__(self, address):
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(address)

    def set_offset(self, val):
        self.instrument.write(f'VOLT:OFFS {val}')

    def close(self):
        self.instrument.close()

    def snapshot(self, update=False):
        """
        Returns a dictionary representing the current state of the device.
        """
        # Example: Return an empty dictionary if the device state cannot be queried
        return {}


