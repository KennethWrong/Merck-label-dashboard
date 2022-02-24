from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from schema import Sample, get_database_uri
import datetime

DATABASE_URI = get_database_uri()
db = create_engine(DATABASE_URI) 
Session = sessionmaker(db) 
session = Session()

############################################################
# Function_name: insert_new_sample
#
# Function_logic:
# This function is invoked after we have checked that the entry is unique to the db.
# 
#
# Arguments: 
#   - qr_code_key: Unique Identfier (PK) for each entry of the database
#   - sample_obj: Object which is what the scientist entered into the fourm in our front-end
#
# Return:
#    - Return current UTC time
############################################################
def insert_new_sample(qr_code_key, sample_obj):
    experiment_id = str(sample_obj['experiment_id'])
    storage_condition = str(sample_obj['storage_condition'])
    analyst = str(sample_obj['analyst'])
    expiration_date = get_strf_utc_date(sample_obj['expiration_date'])
    date_entered = get_strf_utc_date(sample_obj['date_entered'])
    contents = sample_obj['contents']
    date_modified = get_strf_utc_date()

    try:
        new_sample = Sample(qr_code_key = qr_code_key,
                                experiment_id = experiment_id,
                                storage_condition = storage_condition,
                                contents = contents,
                                analyst = analyst,
                                date_entered = date_entered,
                                date_modified = date_modified,
                                expiration_date = expiration_date
                                )
        session.add(new_sample)
        session.commit()
    except Exception as e:
        print(e)
        print('Something went wrong when trying to insert a new sample into the database',flush=True)
    
    return True

############################################################
# Function_name: update_sample_by_qr_code_key
#
# Function_logic:
# These function is invoked when the user tries to create a new entry but an 
#existing entry already exists.
#
# We update all the fields of the entry to make sure that we cover the change they want
#
# Arguments: 
#   - qr_code_key: Unique Identfier (PK) for each entry of the database
#   - sample_obj: Object which is what the scientist entered into the fourm in our front-end
#
# Return:
#    - Return current UTC time
############################################################
def update_sample_by_qr_code_key(qr_code_key, sample_obj):
    experiment_id = str(sample_obj['experiment_id'])
    storage_condition = str(sample_obj['storage_condition'])
    analyst = str(sample_obj['analyst'])
    expiration_date = get_strf_utc_date(sample_obj['expiration_date'])
    date_entered = get_strf_utc_date(sample_obj['date_entered'])
    contents = sample_obj['contents']
    date_modified = get_strf_utc_date()

    try:
        session.query(Sample).filter(Sample.qr_code_key == qr_code_key).\
                    update({
                            Sample.qr_code_key: qr_code_key,
                            Sample.experiment_id: experiment_id,
                            Sample.storage_condition: storage_condition,
                            Sample.contents: contents,
                            Sample.analyst: analyst,
                            Sample.date_entered: date_entered,
                            Sample.date_modified: date_modified,
                            Sample.expiration_date: expiration_date
                            }
                            , synchronize_session = False)
        session.commit()
    except Exception as e:
        print(e)
        print('something went wrong when trying to update an existing entry by its QR_CODE_KEY',flush=True)


############################################################
# Function_name: retrieve_sample_information_with_key
#
# Function_logic:
# Retrieves from the database using the qr_code_key provided to us
#
#
# Arguments: 
#   - qr_code_key: Unique Identfier (PK) for each entry of the database
#
# Return:
#    - Return current UTC time
############################################################
def retrieve_sample_information_with_key(qr_code_key):
    try:
        res = session.query(Sample).filter(Sample.qr_code_key == qr_code_key).first()
    except Exception as e:
        print(e)
        print("Something went wrong when attempting to retrieve a sample from the database \
            using the QR_CODE_KEY. Check if the QR_CODE_KEY being passed is of correct format",flush=True)
    return res



############################################################
# Function_name: check_if_key_exists
#
# Function_logic:
# Given the qr_code_key we check if a row with this key exists, if it does
# we return True, else we return False
#
# Arguments: 
#    - qr_code_key: Unique identifier for each sample. qr_code_key is the Primary Key of each sample in DB
#
# Return:
#    - Bool: True meaning that qr_code_key exists, False meaning that it doesn't
############################################################
def check_if_key_exists(qr_code_key):
    try:
        res = session.query(Sample.qr_code_key).filter_by(qr_code_key=qr_code_key).first()
        return True
    except Exception as e:
        print(e)
        print('Something went wrong when checking if entry exists. Check the format of the QR_Code_key being passed.',flush=True)
    return False



############################################################
# Function_name: get_strf_utc_time
#
# Function_logic:
#Creates a formatted string of the current utc time
#
# Arguments: 
#
# Return:
#    - Return current UTC time
############################################################
def get_strf_utc_date(input=''):
    current_utc = datetime.date.today()
    if input:
            try:
                    current_utc = datetime.datetime.strptime(input,"%m/%d/%Y").date()
            except Exception as e:
                    print(e)
                    print('Please enter correct date format MM/DD/YYYY.',flush=True)

    return current_utc