from flask import Flask,send_from_directory, request, send_file
import api_helper
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import qr_code
import datetime
import os
from PIL import Image
from io import BytesIO, StringIO
import base64
import re

app = Flask(__name__, static_url_path='')
CORS(app)

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
    current_utc = datetime.datetime.utcnow()
    content['date_entered'] = current_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    content['expiration_date'] = current_utc + datetime.timedelta(days=14)
    qr = qr_code.create_qr_code(content)

    #insert sample and information into qr_code
    api_helper.insert_new_sample(qr, content)
    response = api_helper.create_response(qr)
    return response

#Return generated .png of qr_code to the front-end
@app.route('/assets/qr_code/<qr_code_key>',methods=['GET'])
def get_qr_code(qr_code_key):
    return send_file(f"qr_codes/{qr_code_key}.png", mimetype='image/png')

#For front-end sending CSV to backend
@app.route('/csv',methods=['POST'])
def dump_csv():
    #Get the file from the JSON
    file = request.files['csv']
    filename = secure_filename(file.filename)
    #Get path of the csv file to place .csv file into the folder
    print(os.getcwd())
    dir_path = os.path.join(os.getcwd(),'csv')
    full_path = os.path.join(dir_path,f"{filename}")
    #Save the file
    file.save(full_path)
    values = [0,0]
    res = api_helper.parse_csv_to_db(full_path,values)
    return api_helper.create_response(status_code=res, message=f"Total Entries:{values[0]+values[1]} New:{values[0]} Updated:{values[1]}")

#/upload/label_image
@app.route('/upload/label_image', methods=['POST'])
def upload_label_image():
    image_data = re.sub('^data:image/.+;base64,', '', request.form['file'])
    image_title = datetime.datetime.utcnow().strftime("%m-%d-%Y_%H:%M:%S")

    with open(f'/server/images/{image_title}.jpg','wb') as fh:
        fh.write(base64.b64decode(image_data))
    return api_helper.create_response()


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    # app.run(debug=True, port=5000)
