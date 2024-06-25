
import numpy as np
from my_devs import station, dac_adc
from time import sleep
from qcodes import load_or_create_experiment
from qcodes import Parameter
from qcodes import Measurement
from tqdm import tqdm


exp = load_or_create_experiment(experiment_name='MOSFETs', sample_name='test_sample')




dac_adc.get_device_id()
dac_adc.is_device_ready()

###################################################3

# SET CONSTANT VOLTAGES OF THE DAC
dac_adc.set_voltage(2, 0)
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

# START THE MEASUREMENT


with meas.run() as datasaver:
    for set_point in tqdm(np.linspace(-1,1,50)):
        dac_voltage(set_point)
        sleep(0.1)
        x.append(set_point)
        y.append(adc_voltage())
        datasaver.add_result((dac_voltage,set_point),(adc_voltage,adc_voltage()))

#####################################################


#####################################################

# SAVE THE DATA FOR MATPLOTLIB

combined1 = np.column_stack((x,y))
np.savetxt('./GRAPHS/MOSFET/outside_4u.txt',combined1) #For the name: Pressure, temperature and channel length(new/old design)
dac_adc.set_voltage(0, 0)
dac_adc.set_voltage(2, 0)
dac_adc.close()

