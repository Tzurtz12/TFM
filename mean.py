#import serial
import numpy as np
from my_devs import li,station, dac_adc, agilent
from time import sleep
from qcodes import load_or_create_experiment
from qcodes import Parameter
from qcodes import Measurement
from tqdm import tqdm

li.sensitivity(500e-15)

y = []
for _ in range(10000):
    y.append(li.R())

y = np.array(y)
average = np.mean(y)
print(average)

