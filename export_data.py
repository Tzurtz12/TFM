"""
This file contains the functions to export the data from qcodes experimental runs. My codes
already applied lines to create lists and .txt files to save data but this way is more comfortable
and efficient. Also, you avoid overwriting files and save only the important data.
"""

from qcodes import load_by_run_spec
from qcodes.dataset.sqlite.database import initialise_or_create_database_at
import numpy as np


initialise_or_create_database_at('C:/Users/urtzi/experiments.db')

def export_data(id,export_loc):
    name = f'experiment_{id}.csv'
    dataset = load_by_run_spec(captured_run_id=id)
    dataset.write_data_to_text_file(export_loc,single_file=True,single_file_name=name)



id = 350
export_loc = 'C:/Users/urtzi/Desktop/pend/TFM/UB/Qcodes/TFM/GRAPHS/SET'


export_data(id,export_loc)