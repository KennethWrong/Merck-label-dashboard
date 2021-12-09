from flask import make_response
import sqlite3
import pandas as pd
import qr_code
import datetime

#Function for creating return responses for our backend
def create_response(message='',status_code=200, mimetype='application/json'):
        response = make_response(message)
        response.status_code = status_code
        response.mimetype = mimetype
        return response

# Insert new sample from fourm into our database
def insert_new_sample(qr_code_key,json, date):
    conn = sqlite3.connect('data/database.db')
    cur = conn.cursor()

    qr_code_key = str(qr_code_key)
    sample_id = str(json['sample_id'])
    batch_id = str(json['batch_id'])
    protein_concentration = str(json['protein_concentration'])

    cur.execute("INSERT INTO samples (qr_code_key, sample_id, batch_id, protein_concentration, date_entered) VALUES (?,?,?,?,?)",
                (qr_code_key,sample_id,batch_id,protein_concentration, date))

    conn.commit()
    conn.close()
    return

#Uses qr_code key to retrieve sample information from the database
def retrieve_sample_information_with_key(qr_code_key):
        conn = sqlite3.connect('data/database.db')
        cur = conn.cursor()
        return_dic = {}

        qr_code_key = str(qr_code_key)

        cur.execute("SELECT * FROM samples WHERE qr_code_key=?",
                        (qr_code_key,))
        
        res = cur.fetchall()
        conn.commit()
        conn.close()

        content = res[0]

        return_dic['qr_code_key'] = content[0]
        return_dic['sample_id'] = content[1]
        return_dic['batch_id'] = content[2]
        return_dic['protein_concentration'] = content[3]
        return_dic['date_entered'] = content[4]

        return return_dic

#Parse the CSV file into the database
def parse_csv_to_db(file_path):
        try:
                df = pd.read_csv(file_path)
                qr_codes = []
                current_utc = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                for index,row in df.iterrows():
                        dic = {
                                'sample_id': row['sample_id'],
                                'batch_id': row['batch_id'],
                                'protein_concentration': row['protein_concentration'],
                        }
                        code = qr_code.create_qr_code(dic, current_utc)
                        qr_codes.append(code)
                qr_codes = pd.DataFrame(qr_codes)
                df['qr_code_key'] = qr_codes

                conn = sqlite3.connect('data/database.db')
                #have to resolve if data types are the same, perhaps change this to a for loop and appending rows 1 by 1
                #When data is the same we simply skip or update
                df.to_sql('samples', conn, index = False, if_exists='append')
                conn.commit()
                conn.close()
                return 200
        except Exception as e:
                print(e)
                return 500
