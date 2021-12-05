from flask import Flask,send_from_directory, request, send_file
import api_helper
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import qr_code
import datetime
import os

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/',methods=['GET'])
def home():
    return 'This is how routing works'

#This is only for deployment to test our code
# @app.route('/')
# def home():
#     return send_from_directory(app.static_folder,'index.html')

@app.route('/scan/qr_code', methods=['POST'])
def get_vile_info_from_qr_code():
    content = request.json
    qr_code_key = content['qr_code_key']
    info = api_helper.retrieve_sample_information_with_key(qr_code_key)

    response = api_helper.create_response(info)
    return response

@app.route('/create/qr_code', methods=['POST'])
def create_qr_code():
    content = request.json
    current_utc = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    qr = qr_code.create_qr_code(content, current_utc)

    #insert sample and information into qr_code
    api_helper.insert_new_sample(qr, content, current_utc)
    response = api_helper.create_response(qr)
    return response

@app.route('/assets/qr_code/<qr_code_key>',methods=['GET'])
def get_qr_code(qr_code_key):
    return send_file(f'qr_codes/{qr_code_key}.png', mimetype='image/png')

@app.route('/csv',methods=['POST'])
def dump_csv():
    file = request.files['csv']
    filename = secure_filename(file.filename)
    dir_path = os.path.join(os.getcwd(),'csv')
    full_path = os.path.join(dir_path,f"{filename}")
    file.save(full_path)
    res = api_helper.parse_csv_to_db(full_path)
    
    return api_helper.create_response(status_code=res)


if __name__ == '__main__':
    app.run(debug=True,port=5000)