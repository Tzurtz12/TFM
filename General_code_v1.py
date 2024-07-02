#I will try to create a general code to perform every operation with the DAC_ADC
"""
Created 10/05/2024
@author Urtzi Jauregi Aberasturi
"""


import serial
import time
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from tqdm import tqdm

#ser = serial.Serial('/dev/ttyACM0',115200,timeout=1) #Find serial port
ser = serial.Serial('COM10',115200,timeout=1) #Find serial port
time.sleep(2)
if not ser.isOpen():
    print("opened")
    ser.open()

def send_command(command):
    ser.write(command)
    response = ser.readline()
    if command == b"*RDY?\n\r" or b'*IDN?\n\r':
        print(response.decode())

# Operation to get device identification
def get_device_id():
    ser.write(b'*IDN?\n\r')
    print((ser.readline()).decode('utf-8', errors='ignore'))

# Operation to check if device is ready
def is_device_ready():
    ser.write(b"*RDY?\n\r")
    print((ser.readline()).decode('utf-8', errors='ignore'))

# Operation to set voltage to a channel
def set_voltage(channel, voltage):
    channel = str(channel)
    voltage=str(voltage)
    command = "SET\n,\n"+channel+"\n,\n"+voltage+"\n\r"
    ser.write(command.encode())
    #print((ser.readline()).decode('utf-8', errors='ignore'))

# Operation to get voltage read by an input channel
def get_adc_voltage(channel):
    channel = str(channel)
    command = "GET_ADC\n,\n"+channel+"\n\r"
    ser.write(command.encode())
    voltage = (ser.readline()).decode('utf-8', errors='ignore').split()
    #voltage = float(voltage[0])
    print(voltage)
    #return voltage

# Operation to ramp one channel from an initial voltage to a final voltage
def ramp_channel(channel, initial_voltage, final_voltage, num_steps, delay_microseconds):
    
    channel = str(channel)
    initial_voltage = str(initial_voltage)
    final_voltage = str(final_voltage)
    num_steps = str(num_steps)
    delay_microseconds = str(delay_microseconds)
    command = "RAMP1\n,\n"+channel+"\n,\n"+initial_voltage+"\n,\n"+final_voltage+"\n,\n"+num_steps+"\n,\n"+delay_microseconds+"\n\r"
    ser.write(command.encode())

# Operation to ramp two channels from initial voltages to final voltages
def ramp_channels(channel1, channel2, initial_voltage1, initial_voltage2, final_voltage1, final_voltage2, num_steps, delay_microseconds):
    channel1 = str(channel1)
    channel2 = str(channel2)
    initial_voltage1 = str(initial_voltage1)
    initial_voltage2 = str(initial_voltage2)
    final_voltage1 = str(final_voltage1)
    final_voltage2 = str(final_voltage2)
    num_steps = str(num_steps)
    delay_microseconds = str(delay_microseconds)
    command = "RAMP2\n,\n"+channel1+"\n,\n"+channel2+"\n,\n"+initial_voltage1+"\n,\n"+initial_voltage2+"\n,\n"+final_voltage1+"\n,\n"+final_voltage2+"\n,\n"+num_steps+"\n,\n"+delay_microseconds+"\n\r"
    ser.write(command.encode())

# Operation to ramp specified output channels and read specified input channels in a synchronized manner
def buffer_ramp(dac_channels, adc_channels, initial_voltages, final_voltages, num_steps, delay_microseconds, num_readings_to_avg):
    """
    This function is the one we will use for the characterization of SETS as we can do several sweeps at the same time
    and synchronously measure signals using the ACD.
    To insert the channels we want to use for the DAC and ADC we will need to introduce a list.
    For example to use channels 0,1 and 2 --> [0,1,2] will be the introduced list.

    To perform the sweep the order of the introduced voltages will be the same as the one we introduced
    at the DAC. Equally, we will be using a list so having chosen DAC channels "012" I will have initial voltages
    [0,-1,-2] and final voltages [4,2,5] the next way. CH0 [0,4]; CH1 [-1,2] and CH2 [-2,5].
    
    num_steps will be introduced asan integer such as delay_microseconds and num_readings_to_avg.
    """
    dac_channel_str = ''.join(str(channel)for channel in dac_channels)
    adc_channel_str = ''.join(str(channel)for channel in adc_channels)
    initial_voltages_str = ','.join(str(v) for v in initial_voltages)
    final_voltages_str = ','.join(str(v) for v in final_voltages)
    num_steps = str(num_steps) 
    delay_microseconds = str(delay_microseconds)
    num_readings_to_avg = str(num_readings_to_avg)
    command = "BUFFER_RAMP\n,\n"+dac_channel_str+"\n,\n"+adc_channel_str+"\n,\n"+initial_voltages_str+"\n,\n"+final_voltages_str+"\n,\n"+num_steps+"\n,\n"+delay_microseconds+"\n,\n"+num_readings_to_avg+"\n\r"
    ser.write(command.encode())
    print((ser.readline()).decode('utf-8', errors='ignore'))

def convert_time(channel,time):
    channel = str(channel)
    time=str(time)
    command = "CONVERT_TIME\n,\n"+channel+"\n,\n"+time+"\n\r"
    ser.write(command.encode())

is_device_ready()
get_device_id()

set_voltage(0,0)
set_voltage(1,0)
set_voltage(2,0)
set_voltage(3,0)
ser.close()
print("ended")