#import serial
import matplotlib.pyplot as plt
import numpy as np
from my_devs import li,station
from time import sleep
from qcodes import load_or_create_experiment
from qcodes import Parameter
from qcodes import Measurement
from tqdm import tqdm
from qcodes.dataset import LinSweep


exp = load_or_create_experiment(experiment_name='lockin_test', sample_name='test_sample')




meas = Measurement(exp=exp, station=station)
meas.register_parameter(li.amplitude,paramtype='array')
meas.register_parameter(li.R,setpoints=(li.amplitude,),paramtype='array')
initial_val = 0.05
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
li.sensitivity(sensitivity_list[i])
with meas.run() as datasaver:
    for set_point in tqdm(np.linspace(initial_val,1,1000)):
        li.amplitude(set_point)
        sleep(0.1)
        if li.sensitivity() <= 1.15*li.R():
            i+=1
            li.sensitivity(sensitivity_list[i])
        datasaver.add_result((li.amplitude,set_point),(li.R,li.R()))
    dataset = datasaver.dataset 