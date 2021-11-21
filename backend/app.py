from flask import Flask,send_from_directory, request, send_file
import api_helper
from flask_cors import CORS, cross_origin
import qr_code

app = Flask(__name__, static_url_path='', static_folder='../frontend/build')
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
    print(content)
    qr_code_key = content['qr_code_key']
    response = api_helper.create_response(qr_code_key)
    return response

@app.route('/create/qr_code', methods=['POST'])
def create_qr_code():
    content = request.json
    qr = qr_code.create_qr_code(content)
    print(f"In route {qr}")
    response = api_helper.create_response(qr)
    return response

@app.route('/assets/qr_code/<qr_code_key>',methods=['GET'])
def get_qr_code(qr_code_key):
    return send_file(f'qr_codes/{qr_code_key}.png', mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True,port=5000)