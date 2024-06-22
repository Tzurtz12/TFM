#import serial
import matplotlib.pyplot as plt
import numpy as np
from my_devs import li,station, dac_adc
from time import sleep
from qcodes import load_or_create_experiment
from qcodes import Parameter
from qcodes import Measurement
#from qcodes import LinSweep
from tqdm import tqdm
from qcodes.dataset import LinSweep
from DAC_ADC import DAC_ADC


exp = load_or_create_experiment(experiment_name='lockin_test', sample_name='test_sample')



#dac_adc = DAC_ADC(port='COM10', baudrate=115200, timeout=1)

dac_adc.get_device_id()
dac_adc.is_device_ready()




meas = Measurement(exp=exp, station=station)
dac_voltage = Parameter('dac_voltage', set_cmd=lambda val: dac_adc.set_voltage(0, val),get_cmd=None)
meas.register_parameter(dac_voltage)
dac_voltage2 = Parameter('dac_voltage2', set_cmd=lambda val: dac_adc.set_voltage(2, val),get_cmd=None)
meas.register_parameter(dac_voltage2)
adc_voltage = Parameter('adc_voltage', get_cmd=lambda: dac_adc.get_adc_voltage(3))
meas.register_parameter(li.amplitude,paramtype='array')
meas.register_parameter(adc_voltage,setpoints=(dac_voltage,dac_voltage2))

meas.register_parameter(li.R,setpoints=(li.amplitude,),paramtype='array')
initial_val = 0.007
li.amplitude(initial_val)
sleep(1)
sensitivity = {
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
sensitivity_list = list(sensitivity.keys())
i = 11
x1 = []
x2 = []
y  = []
li.sensitivity(sensitivity_list[i])
with meas.run() as datasaver:
    for set_point in tqdm(np.linspace(initial_val,4,10)):
        dac_voltage(set_point)
        for set_point2 in np.linspace(0,4,20):
            #li.amplitude(set_point)
            dac_voltage2(set_point2)
            sleep(0.1)
            if set_point2 >2 and set_point > 2:
                dac_adc.set_voltage(3, 0.5)
                sleep(0.1)
            else:
                dac_adc.set_voltage(3, np.random.rand()/2)
                sleep(0.1)
            
            adc_val =adc_voltage()
            x2.append(set_point)
            x1.append(set_point2)
            y.append(adc_val)
            # if li.sensitivity() <= 1.15*li.R() and i < 26:
            #     i+=1
            #     li.sensitivity(sensitivity_list[i])
            #     sleep(0.1)
            #datasaver.add_result((li.amplitude,set_point),(li.R,li.R())) 
            datasaver.add_result((dac_voltage,set_point),(dac_voltage2,set_point2),(adc_voltage,adc_val)) 

combined1 = np.column_stack((x1,x2,y))
# combined2 = np.column_stack((x1,y2))
np.savetxt('./GRAPHS/diamonds1.txt',combined1)
# np.savetxt('./GRAPHS/combined2.txt',combined2)

dac_adc.close()

