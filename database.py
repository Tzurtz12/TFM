from qcodes import initialise_or_create_database_at

DATABASE_LOCATION = "./exp.db"



initialise_or_create_database_at(db_file_with_abs_path=DATABASE_LOCATION)