'''
This one is just to create the database at our desired location
'''
from qcodes import initialise_or_create_database_at

DATABASE_LOCATION = "./exp.db" 



initialise_or_create_database_at(db_file_with_abs_path=DATABASE_LOCATION)