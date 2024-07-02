from agilent_33220a import Agilent_33220A
import numpy as np
from time import sleep
device = Agilent_33220A('GPIB0::30::INSTR')
# for val in np.linspace(0, 0.2, 100):
#     device.set_offset(val)
#     sleep(0.1)

device.set_offset(0.75e-3)  # Set offset to 1.0 volts