from flask import Flask,send_from_directory

app = Flask(__name__, static_url_path='', static_folder='../frontend/build')


@app.route('/',methods=['GET'])
def home():
    return 'This is how routing works'

# @app.route('/')
# def home():
#     return send_from_directory(app.static_folder,'index.html')

if __name__ == '__main__':
    app.run(debug=True,port=5000)