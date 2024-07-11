''''
I just created this file to be sure the DAC_ADC class is working properly.
'''

from DAC_ADC import DAC_ADC
import numpy as np
device = DAC_ADC(port='COM10', baudrate=115200, timeout=1)

device.get_device_id()
device.is_device_ready()

device.set_voltage(3, 1.6) ## 3 the channel we want to use. 1.6 the voltage value
print(device.get_adc_voltage(2)) # to get the adc value just introduce the channel. 2 in this case

device.convert_time(2000) #ADC time constant in microseconds. Maximum in 2686 microseconds.

device.ramp_channel(1, 0, 1, 1000, 1000) # channel, initial voltage, final voltage, number of steps, delay in microseconds
device.ramp_channels(1, 2, 0, 0.5, 1, 2, 1000, 1000) # channel1, channel2, initial_voltage1, initial_voltage2, final_voltage1, final_voltage2, num_steps, delay_microseconds

device.buffer_ramp([1, 2], [0,3],[0, 1], [1, 0], 1000, 1000,1) # dac channels, adc channels, initial voltages, final voltages, number of steps, delay in microseconds and average
device.close()

