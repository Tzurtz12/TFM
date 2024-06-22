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

###################################################3

# SET CONSTANT VOLTAGES OF THE DAC

#####################################################

#####################################################

# REGISTER THE PARAMETER FOR QCODES PLOTTING

meas = Measurement(exp=exp, station=station)
dac_voltage = Parameter('dac_voltage', set_cmd=lambda val: dac_adc.set_voltage(0, val),get_cmd=None)
meas.register_parameter(dac_voltage)
#dac_voltage2 = Parameter('dac_voltage2', set_cmd=lambda val: dac_adc.set_voltage(2, val),get_cmd=None)
#meas.register_parameter(dac_voltage2)
adc_voltage = Parameter('adc_voltage', get_cmd=lambda: dac_adc.get_adc_voltage(2))
#meas.register_parameter(li.amplitude,paramtype='array')
meas.register_parameter(adc_voltage,setpoints=(dac_voltage,))#,dac_voltage2))
#meas.register_parameter(li.R,setpoints=(dac_voltage,),paramtype='array')

#####################################################


#####################################################

# SET THE INITIAL VALUES OF THE LOCK-IN AMPLIFIER SENSITIVITY

#initial_val = 0.007
# li.amplitude(0.066)
# li.time_constant(300e-3)
# #
x = []
y  = []
#li.sensitivity(1e-9)


#####################################################

# START THE MEASUREMENT


with meas.run() as datasaver:
    for set_point in tqdm(np.linspace(-1,1,50)):
        dac_voltage(set_point)
        sleep(0.1)
        x.append(set_point)
        y.append(adc_voltage()/1e5)
        # if li.sensitivity() <= 1.15*li.R() and i < 26:
        #     i+=1
        #     li.sensitivity(sensitivity_list[i])
        #     sleep(0.1)
        #datasaver.add_result((dac_voltage,set_point),(li.R,li.R())) 
        datasaver.add_result((dac_voltage,set_point),(adc_voltage,adc_voltage()))

#####################################################


#####################################################

# SAVE THE DATA FOR MATPLOTLIBÇ

combined1 = np.column_stack((x,y))
# combined2 = np.column_stack((x1,y2))
np.savetxt('./GRAPHS/mosfet_28k_dc_gate_source.txt',combined1)
# np.savetxt('./GRAPHS/combined2.txt',combined2)
dac_adc.set_voltage(0, 0)
dac_adc.set_voltage(2, 0)
dac_adc.close()

