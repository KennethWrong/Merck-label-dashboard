from flask import Flask, request, send_from_directory, redirect
import api_helper
from flask_cors import CORS
from werkzeug.utils import secure_filename
from api_helper import print_label_with_qr_code_key
import qr_code
import os
import base64
import re
import uuid
import db_helper

redirect_url = "http://localhost:5000/"

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
app.config['DEBUG']=True
app.config['CORS_HEADERS'] = 'application/json'
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return send_from_directory(app.static_folder, 'index.html')

#End point for qr_code scanning
@app.route('/scan/qr_code', methods=['POST'])
def get_vile_info_from_qr_code():
    content = request.json
    qr_code_key = content['qr_code_key']
    info,status = api_helper.retrieve_sample_information_with_key(qr_code_key)
    response = api_helper.create_response_from_scanning(info, status_code=status)
    return response

#End point for creating qr_code
@app.route('/create/qr_code', methods=['POST'])
def create_qr_code():
    content = request.json
    #With the qr_code_size we can call create qr_code small, medium large
    qr_code_key, image_base64  = qr_code.create_qr_code_without_saving(content)
    # qr = qr_code.create_qr_code(content)

    #insert sample and information into qr_code
    api_helper.insert_new_sample(qr_code_key, content)

    message = {
        'qr_code_key': qr_code_key,
        'image_string': image_base64,
    }

    status = 200 if image_base64 != None else 500

    return api_helper.create_response_from_scanning(message=message, status_code=status)

#For printing qr_code
@app.route('/print/<qr_code_key>',methods=['GET'])
def print_label(qr_code_key):
    size = request.args.get('size')
    status = print_label_with_qr_code_key(qr_code_key, size)
    return api_helper.create_response(status_code=status, message="printing success")

#For front-end sending CSV to backend
@app.route('/csv',methods=['POST'])
def dump_csv():
    #Get the file from the JSON
    file = request.files['csv']
    filename = secure_filename(file.filename)
    #Get path of the csv file to place .csv file into the folder
    dir_path = os.path.join(os.getcwd(),'backend','csv')
    full_path = os.path.join(dir_path,f"{filename}")
    #Save the file
    file.save(full_path)
    values = [0,0]
    status, dic = api_helper.parse_csv_to_db(full_path,values)
    dic['message'] = f"Total Entries:{values[0]+values[1]} New:{values[0]} Updated:{values[1]}"
    return api_helper.create_response_from_scanning(status_code=status, message=dic)

@app.route('/asset/<qr_code_key>',methods=['GET'])
def get_qr_code_image(qr_code_key):
    base64_image = api_helper.retrieve_label_with_qr_code_key(qr_code_key)
    status_code = 200 if base64_image else 500
    return_dic = {
        'image':base64_image
    }
    return api_helper.create_response_from_scanning(status_code=status_code, message=return_dic)


#/upload/label_image
@app.route('/upload/label_image', methods=['POST'])
def upload_label_image():
    image_data = re.sub('^data:image/.+;base64,', '', request.form['file'])
    image_title = db_helper.get_strf_utc_date().strftime("%m-%d-%Y") +"-"+ str(uuid.uuid4())[3:8]

    with open(f'/server/images/{image_title}.jpg','wb') as fh:
        fh.write(base64.b64decode(image_data))
    return api_helper.create_response()


#for redirecting


@app.route('/scan/qr_code', methods=['GET'])
def redirect_get_vile_info_from_qr_code():
    return redirect(redirect_url, code=302)

@app.route('/create/qr_code', methods=['GET'])
def redirect_qr_code():
    return redirect(redirect_url, code=302)

@app.route('/QRScanner', methods=['GET'])
def redirect_qr_scanner():
    return redirect(redirect_url, code=302)

@app.route('/csv_upload', methods=['GET'])
def redirect_csv_upload():
    return redirect(redirect_url, code=302)

@app.route('/lookup', methods=['GET'])
def redirect_lookup():
    return redirect(redirect_url, code=302)
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
