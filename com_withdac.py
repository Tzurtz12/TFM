''''
I just created this file to be sure the DAC_ADC class is working properly.
'''

from DAC_ADC import DAC_ADC
import numpy as np
device = DAC_ADC(port='COM10', baudrate=115200, timeout=1)

device.get_device_id()
device.is_device_ready()

device.set_voltage(3, 1.654)
print(device.get_adc_voltage(1))
device.close()