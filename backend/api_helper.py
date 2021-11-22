from flask import make_response
import sqlite3

def create_response(message='',status_code=200, mimetype='application/json'):
        response = make_response(message)
        response.status_code = status_code
        response.mimetype = mimetype
        return response

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

def retrieve_sample_information_with_key(qr_code_key):
        conn = sqlite3.connect('data/database.db')
        cur = conn.cursor()
        return_dic = {}

        qr_code_key = str(qr_code_key)
        print(qr_code_key)

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