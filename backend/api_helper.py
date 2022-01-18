from flask import make_response
import sqlite3
import pandas as pd
import qr_code
from schema import samples
from datetime import datetime
from sqlalchemy import create_engine, select
import os

db_path = os.path.join(os.getcwd(),'data','database.db')
engine = create_engine(f'sqlite:///{db_path}')

#Function for creating return responses for our backend
def create_response(message='',status_code=200, mimetype='application/json'):
        response = make_response(message)
        response.status_code = status_code
        response.mimetype = mimetype
        return response

# Insert new sample from fourm into our database
def insert_new_sample(qr_code_key,json):
    qr_code_key = str(qr_code_key)
    sample_id = str(json['sample_id'])
    batch_id = str(json['batch_id'])
    protein_concentration = str(json['protein_concentration'])
    exists = check_if_key_exists(qr_code_key)
    conn = engine.connect()
    if exists:
            sql = samples.update().values(sample_id=sample_id,batch_id=batch_id,protein_concentration=protein_concentration).\
                    where(samples.c.qr_code_key == qr_code_key)
            conn.execute(sql)
            conn.close()
            return False
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
    

#Uses qr_code key to retrieve sample information from the database
def retrieve_sample_information_with_key(qr_code_key):
        conn = sqlite3.connect('data/database.db')
        return_dic = {}
        qr_code_key = str(qr_code_key)

        conn = engine.connect()
        sql = select([samples]).where((samples.c.qr_code_key == qr_code_key))
        res = conn.execute(sql)
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

def check_if_key_exists(qr_code_key):
        conn = engine.connect()
        sql = select([samples]).where((samples.c.qr_code_key == qr_code_key))
        res = conn.execute(sql)
        res = res.fetchall()
        
        return True if len(res) > 0 else False


#Parse the CSV file into the database
def parse_csv_to_db(file_path,info):
        conn = engine.connect()
        try:
                df = pd.read_csv(file_path)
                updated, added = 0,0
                qr_codes = []
                current_utc = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                for index,row in df.iterrows():
                        dic = {
                                'sample_id': str(row['sample_id']),
                                'batch_id': str(row['batch_id']),
                                'protein_concentration': str(row['protein_concentration']),
                        }
                        qr_code_key = qr_code.create_qr_code(dic, current_utc)
                        if insert_new_sample(qr_code_key, dic):
                                info[0] += 1
                        else:
                                info[1] += 1
                conn.close()
                return 200
        except Exception as e:
                print(e)
                return 500
