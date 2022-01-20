from importlib.machinery import DEBUG_BYTECODE_SUFFIXES
from flask import make_response
import pandas as pd
import qr_code
from schema import samples
from datetime import datetime
from sqlalchemy import create_engine, select
import os

##These two lines of code will change oncce we get our online PostGreSQL
#Find the local database in file system
db_path = os.path.join(os.getcwd(),'data','database.db')
#Creates a SQLAlchemy engine to perform CRUD on DB
engine = create_engine(f'sqlite:///{db_path}')


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
    qr_code_key = str(qr_code_key)
    sample_id = str(sample_obj['sample_id'])
    batch_id = str(sample_obj['batch_id'])
    protein_concentration = str(sample_obj['protein_concentration'])

    #Checks if this qr_code_key created already exists in our DB. Returns True if exists
    exists = check_if_key_exists(qr_code_key)

    #Creating a connection obj by connecting to our DB so that we can perform CRUD
    conn = engine.connect()

    #Updates existing sample if qr_code exists in our DB
    if exists:
            sql = samples.update().values(sample_id=sample_id,batch_id=batch_id,protein_concentration=protein_concentration).\
                    where(samples.c.qr_code_key == qr_code_key)
            conn.execute(sql)
            conn.close()
            return False
    #If sample inserting to DB is unique
    else:
        conn.execute(samples.insert(), [
                {
                        'qr_code_key':qr_code_key,
                        'sample_id':sample_id,
                        'batch_id':batch_id,
                        'protein_concentration': protein_concentration,
                }
        ])
    conn.close()
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

        conn = engine.connect()
        sql = select([samples]).where((samples.c.qr_code_key == qr_code_key))
        res = conn.execute(sql)

        # Needs error handelling in the case that the qr_code_key does not exist in DB
        res = res.fetchall()
        content = res[0]

        return_dic = {
                'qr_code_key': content[0],
                'sample_id': content[1],
                'batch_id': content[2],
                'protein_concentration': content[3],
                'date_entered': content[4],
        }
        conn.close()

        return return_dic


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
        conn = engine.connect()
        sql = select([samples]).where((samples.c.qr_code_key == qr_code_key))
        res = conn.execute(sql)
        res = res.fetchall()
        
        return True if len(res) > 0 else False


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
        conn = engine.connect()
        try:
                df = pd.read_csv(file_path)
                current_utc = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                for index,row in df.iterrows():

                        #Convert dataframe rows into a JSON obj (dictionary)
                        dic = {
                                'sample_id': str(row['sample_id']),
                                'batch_id': str(row['batch_id']),
                                'protein_concentration': str(row['protein_concentration']),
                        }

                        qr_code_key = qr_code.create_qr_code(dic, current_utc)
                        #If we are inserting a new_sample, we update new_sample_insert count
                        if insert_new_sample(qr_code_key, dic):
                                info[0] += 1
                        #If we are inserting an exisiting sample, we update updated_insert_count
                        else:
                                info[1] += 1
                conn.close()
                return 200
        except Exception as e:
                print(e)
                return 500
