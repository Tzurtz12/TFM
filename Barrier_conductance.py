'''
File to perform the barrier conductance experiment. The objective of this
run is measuring the threshold values of the barrier gates. Once measured them, we should set
the barrier voltage below these values in order to create the quantum dot in the channel.
'''
import matplotlib.pyplot as plt
import numpy as np
from my_devs import li,station, dac_adc, agilent
from time import sleep
from qcodes import load_or_create_experiment
from qcodes import Parameter
from qcodes import Measurement
from tqdm import tqdm


#create the experiment. It is important to set the sample name in order to save the data in the properly at .db files
exp = load_or_create_experiment(experiment_name='barrier_conductance', sample_name='Right 40 K')



#Check the dac-adc device is ready to be used

dac_adc.get_device_id()
dac_adc.is_device_ready()

###################################################

# SET CONSTANT VOLTAGES OF THE DAC: One barrier, Vds and Vg

dac_adc.set_voltage(0,1.5) #lead gate above the threshold
dac_adc.set_voltage(3,1.5) #barrier 2 above the threshold
dac_adc.set_voltage(2, 0) # Barrier 1 (we will sweep this one)
dac_adc.set_voltage(1, 0.1) # Vds

#####################################################

#####################################################

# REGISTER THE PARAMETERS FOR QCODES PLOTTING

meas = Measurement(exp=exp, station=station)
barrier_voltage = Parameter('barrier_voltage', set_cmd=lambda val: agilent.set_offset(val) ,get_cmd=None)
meas.register_parameter(barrier_voltage)
meas.register_parameter(li.R,setpoints=(barrier_voltage,),paramtype='array')

#####################################################


#####################################################

# SET THE INITIAL VALUES OF THE LOCK-IN AMPLIFIER SENSITIVITY


li.time_constant(0.3)
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
i = 12
x = []
y  = []
li.sensitivity(20e-12) # 20 pA should be enough. However, we got the index i to change it if necessary


#####################################################

# START THE MEASUREMENT, set initial and final values of the barrier voltage

init = 0
final = 1.5
steps = º



with meas.run() as datasaver:
    for set_point in tqdm(np.linspace(init,final,steps)):
        barrier_voltage(set_point)
        sleep(1)
        x.append(set_point)
        y.append(li.R())
        if li.sensitivity() <= 1.5*li.R():
                i+=1
                li.sensitivity(sensitivity_list[i])
                sleep(0.1)
        datasaver.add_result((barrier_voltage,set_point),(li.R,li.R()))
        for val in np.linspace(final, init, 10):
            barrier_voltage(val) 

#####################################################


#####################################################

# SAVE THE DATA FOR MATPLOTLIB

combined1 = np.column_stack((y,x))
np.savetxt('./GRAPHS/SET/barrier1_left.txt',combined1)


#####################################################

# Set the dac values at 0 to protect the sample

dac_adc.set_voltage(0,0)
dac_adc.set_voltage(1,0)
dac_adc.set_voltage(2,0)
dac_adc.set_voltage(3,0)

dac_adc.close()

