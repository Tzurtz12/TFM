import qcodes as qc
from qcodes.instrument_drivers.stanford_research.SR830 import SR830
from DAC_ADC import DAC_ADC
from qcodes.instrument_drivers.Keithley import Keithley2400

station = qc.Station()

li = SR830(name='lock-in',address='GPIB0::8::INSTR')
dac_adc = DAC_ADC(port='COM10', baudrate=115200, timeout=1)
#keithley2400 = Keithley2400(name='keithley2400', address='GPIB0::22::INSTR')  

station.add_component(li)
station.add_component(dac_adc)
#station.add_component(keithley2400)
