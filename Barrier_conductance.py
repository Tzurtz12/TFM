#import serial
import matplotlib.pyplot as plt
import numpy as np
from my_devs import li,station, dac_adc
from time import sleep
from qcodes import load_or_create_experiment
from qcodes import Parameter
from qcodes import Measurement
from tqdm import tqdm



exp = load_or_create_experiment(experiment_name='barrier_conductance', sample_name='test_sample')



#dac_adc = DAC_ADC(port='COM10', baudrate=115200, timeout=1)

dac_adc.get_device_id()
dac_adc.is_device_ready()

###################################################3

# SET CONSTANT VOLTAGES OF THE DAC: One barrier, Vds and Vg
dac_adc.set_voltage(0, 0)
dac_adc.set_voltage(1, 0)
dac_adc.set_voltage(2, 0)
#####################################################

#####################################################

# REGISTER THE PARAMETER FOR QCODES PLOTTING

meas = Measurement(exp=exp, station=station)
dac_voltage = Parameter('dac_voltage', set_cmd=lambda val: dac_adc.set_voltage(3, val),get_cmd=None)
meas.register_parameter(dac_voltage)

meas.register_parameter(li.R,setpoints=(dac_voltage,),paramtype='array')

#####################################################


#####################################################

# SET THE INITIAL VALUES OF THE LOCK-IN AMPLIFIER SENSITIVITY

#initial_val = 0.007
li.amplitude(0.066)
li.time_constant(300e-3)
sleep(1)
sensitivity_volt = {
        2e-9: 0,
        5e-9: 1,
        10e-9: 2,
        20e-9: 3,
        50e-9: 4,
        100e-9: 5,
        200e-9: 6,
        500e-9: 7,
        1e-6: 8,
        2e-6: 9,
        5e-6: 10,
        10e-6: 11,
        20e-6: 12,
        50e-6: 13,
        100e-6: 14,
        200e-6: 15,
        500e-6: 16,
        1e-3: 17,
        2e-3: 18,
        5e-3: 19,
        10e-3: 20,
        20e-3: 21,
        50e-3: 22,
        100e-3: 23,
        200e-3: 24,
        500e-3: 25,
        1: 26
    }
sensitivity_curr = {
        2e-15: 0,
        5e-15: 1,
        10e-15: 2,
        20e-15: 3,
        50e-15: 4,
        100e-15: 5,
        200e-15: 6,
        500e-15: 7,
        1e-12: 8,
        2e-12: 9,
        5e-12: 10,
        10e-12: 11,
        20e-12: 12,
        50e-12: 13,
        100e-12: 14,
        200e-12: 15,
        500e-12: 16,
        1e-9: 17,
        2e-9: 18,
        5e-9: 19,
        10e-9: 20,
        20e-9: 21,
        50e-9: 22,
        100e-9: 23,
        200e-9: 24,
        500e-9: 25,
        1e-6: 26,
    }

sensitivity_list = list(sensitivity_curr.keys())
i = 23
x = []
y  = []
li.sensitivity(1e-9)


#####################################################

# START THE MEASUREMENT


with meas.run() as datasaver:
    for set_point in tqdm(np.linspace(0,1.5,200)):
        dac_voltage(set_point)
        sleep(0.1)
        x.append(set_point)
        y.append(li.R())
        if li.sensitivity() <= 1.15*li.R() and i < 26:
            i+=1
            li.sensitivity(sensitivity_list[i])
            sleep(0.1)
        elif li.R() < 0.1 * li.sensitivity() and i > 0:
            i-=1
            li.sensitivity(sensitivity_list[i])
            sleep(0.1)
        datasaver.add_result((dac_voltage,set_point),(li.R,li.R())) 
        #datasaver.add_result((dac_voltage,set_point),(adc_voltage,adc_voltage()))

#####################################################


#####################################################

# SAVE THE DATA FOR MATPLOTLIBÇ

combined1 = np.column_stack((x,y))
# combined2 = np.column_stack((x1,y2))
np.savetxt('./GRAPHS/mosfet_28k.txt',combined1)
# np.savetxt('./GRAPHS/combined2.txt',combined2)
dac_adc.set_voltage(0, 0)
dac_adc.set_voltage(2, 0)
dac_adc.close()

