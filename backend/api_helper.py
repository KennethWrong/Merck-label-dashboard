from importlib.machinery import DEBUG_BYTECODE_SUFFIXES
from random import sample
from flask import make_response, json
import pandas as pd
import qr_code
from datetime import datetime, date
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from schema import Sample, get_database_uri

#Creates a session with your local postgresql database
DATABASE_URI = get_database_uri()
db = create_engine(DATABASE_URI) 
Session = sessionmaker(db) 
session = Session()

############################################################
# Function_name: create_response
#
# Function_logic:
# Utilises the make_response function from flask (Check flask documentation for more info)
#
#
# Arguments: 
#    - message (default is ''): Message that we would like to return to our client (Should be in string format)
#    - status_code (default is 200): Indication of whether clients request suceeded, e.g 200, 400, 404
#    -mimetype (default is JSON): mimetype of the content that we are returning to the client
# Return:
#    - response: Response object created from make_response function for us to return response to users.
############################################################
def create_response(message='',status_code=200, mimetype='application/json'):
        response = make_response(message)
        response.status_code = status_code
        response.mimetype = mimetype
        return response

def create_response_from_scanning(message="", status_code=200, mimetype='application/json'):
        response = make_response(json.dumps(message))
        response.status_code = status_code
        response.mimetype = mimetype
        return response


############################################################
# Function_name: insert_new_sample
#
# Function_logic:
# Inserts newly retrieved sample (both from CSV and input form) into our data base.
# Currently it overrites existing data, depends on what Terri wants in terms of duplicate entries
#
# Arguments: 
#    - qr_code_key: Unique identifier for each sample. qr_code_key is the Primary Key of each sample in DB
#    - sample_obj: Obj containing key-value pair of information regarding each sample
# Return:
#    - Bool: Returns True/False on whether our insertion was a duplicate or unique
############################################################
def insert_new_sample(qr_code_key,sample_obj):
    experiment_id = str(sample_obj['experiment_id'])
    storage_condition = str(sample_obj['storage_condition'])
    analyst = str(sample_obj['analyst'])
    expiration_date = get_strf_utc_date(sample_obj['expiration_date'])
    date_entered = sample_obj['date_entered']
    contents = sample_obj['contents']
    date_modified = get_strf_utc_date()

    #Checks if this qr_code_key created already exists in our DB. Returns True if exists
    exists = check_if_key_exists(qr_code_key)
    #Updates existing sample if qr_code exists in our DB
    if exists:
            session.query(Sample).filter(Sample.qr_code_key == qr_code_key).\
                    update({Sample.experiment_id: experiment_id,
                            Sample.storage_condition: storage_condition,
                            Sample.contents: contents,
                            Sample.analyst: analyst,
                            Sample.date_entered: date_entered,
                            Sample.date_modified: date_modified,
                            Sample.expiration_date: expiration_date
                            }
                            , synchronize_session = False)
            session.commit()
            return False
    #If sample inserting to DB is unique
    else:
        new_sample = Sample(qr_code_key = qr_code_key,
                            experiment_id = experiment_id,
                            storage_condition = storage_condition,
                            contents = contents,
                            analyst = analyst,
                            date_entered = date_entered,
                            date_modified = date_entered,
                            expiration_date = expiration_date
                            )
        session.add(new_sample)
        session.commit()

    return True
    

############################################################
# Function_name: retrieve_sample_information_with_key
#
# Function_logic:
# Inserts newly retrieved sample (both from CSV and input form) into our data base.
# Currently it overrites existing data, depends on what Terri wants in terms of duplicate entries
#
# Arguments: 
#    - qr_code_key: Unique identifier for each sample. qr_code_key is the Primary Key of each sample in DB
#
# Return:
#    - return_dic: All columns of sample in the DB
############################################################
def retrieve_sample_information_with_key(qr_code_key):
        return_dic = {}
        qr_code_key = str(qr_code_key)

        res = session.query(Sample).filter(Sample.qr_code_key == qr_code_key).first()
        # if qr_code_key does not exist in DB
        if not res:
                return {}, 404

        else: # qr_code_key exists in DB
                content = res # if res is None, it will say invalid index
        
                return_dic = {
                        'qr_code_key': content.qr_code_key,
                        'experiment_id': content.experiment_id,
                        'storage_condition': content.storage_condition,
                        'analyst': content.analyst,
                        'contents': content.contents,
                        'date_entered': content.date_entered,
                        'date_modified': content.date_modified,
                        'expiration_date': content.expiration_date
                }

        return return_dic, 200


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
        res = session.query(Sample.qr_code_key).filter_by(qr_code_key=qr_code_key).first()
        return True if res else False

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
        if input:
                current_utc = datetime.strptime(input,"%m-%d-%Y").date()
        else:
                current_utc = date.today()
        return current_utc

############################################################
# Function_name: parse_csv_to_db
#
# Function_logic:
# This function is called to parse a CSV uploaded and insert each column of the CSV
# into our DB.
#
# Arguments: 
#    - file_path: The path of the uploaded CSV file that we stored in ../csv
#    - info: info is an array [new_insert_count, updated_insert_count]
#            -> This code just returns to our front-end how many of the rows in the CSV that
#               we inserted into our DB were duplicate or Unique. (Can be removed)
#
# Return:
#    - Status-Code: 200 if successful, 500 if unsuccessful
############################################################
def parse_csv_to_db(file_path,info):
        try:
                df = pd.read_csv(file_path)
                current_date = get_strf_utc_date()
                for index,row in df.iterrows():

                        #Convert dataframe rows into a JSON obj (dictionary)
                        dic = {
                                'experiment_id': row['experiment_id'],
                                'storage_condition': row['storage_condition'],
                                'analyst': row['analyst'],
                                'contents': row['contents'],
                                'date_entered': row['date_entered'],
                                'expiration_date': row['expiration_date'],
                                'date_modified': current_date
                        }

                        qr_code_key = qr_code.create_qr_code(dic)
                        #If we are inserting a new_sample, we update new_sample_insert count
                        if insert_new_sample(qr_code_key, dic):
                                info[0] += 1
                        #If we are inserting an exisiting sample, we update updated_insert_count
                        else:
                                info[1] += 1

                return 200
        except Exception as e:
                print(e)
                return 500
