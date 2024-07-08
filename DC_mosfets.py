'''
File to perform DC sweeps to measure punch-through effect at MOSFETs
'''
import numpy as np
from my_devs import station, dac_adc
from time import sleep
from qcodes import load_or_create_experiment
from qcodes import Parameter
from qcodes import Measurement
from tqdm import tqdm


#exp = load_or_create_experiment(experiment_name='MOSFETs_cold', sample_name='old sample 25K')

exp = load_or_create_experiment(experiment_name='new 3', sample_name='270 K')



dac_adc.get_device_id()
dac_adc.is_device_ready()

###################################################3

# SET CONSTANT VOLTAGES OF THE DAC
dac_adc.set_voltage(2, 0)

dac_adc.convert_time(2,2500)

#####################################################

#####################################################

# REGISTER THE PARAMETER FOR QCODES PLOTTING

meas = Measurement(exp=exp, station=station)
dac_voltage = Parameter('dac_voltage', set_cmd=lambda val: dac_adc.set_voltage(0, val),get_cmd=None)
meas.register_parameter(dac_voltage)
adc_voltage = Parameter('adc_voltage', get_cmd=lambda: dac_adc.get_adc_voltage(2))
meas.register_parameter(adc_voltage,setpoints=(dac_voltage,))

#####################################################


#####################################################

# SET THE INITIAL VALUES OF THE LOCK-IN AMPLIFIER SENSITIVITY


x = []
y  = []
sensitivity = 1e-6

# START THE MEASUREMENT


with meas.run() as datasaver:
    for set_point in tqdm(np.linspace(-2,2,100)):
        dac_voltage(set_point)
        sleep(0.3)
        x.append(set_point)
        y.append(adc_voltage()*sensitivity)
        datasaver.add_result((dac_voltage,set_point),(adc_voltage,adc_voltage()))
        

#####################################################


#####################################################

# SAVE THE DATA FOR MATPLOTLIB

combined1 = np.column_stack((x,y))
np.savetxt('./GRAPHS/MOSFET/new_3_left_270K.txt',combined1) #For the name: Pressure, temperature and channel length(new/old design)
dac_adc.set_voltage(0, 0)
dac_adc.set_voltage(2, 0)
dac_adc.close()