#import serial
import matplotlib.pyplot as plt
import numpy as np
from my_devs import li,station, dac_adc, keithley2400
from time import sleep
from qcodes import load_or_create_experiment
from qcodes import Parameter
from qcodes import Measurement
#from qcodes import LinSweep
from tqdm import tqdm
from qcodes.dataset import LinSweep


exp = load_or_create_experiment(experiment_name='test_curr', sample_name='test_sample')

meas = Measurement(exp=exp, station=station)

meas.register_parameter(keithley2400.curr)
keithley2400.mode('CURR')
keithley2400.output(1)
print(keithley2400.curr())

