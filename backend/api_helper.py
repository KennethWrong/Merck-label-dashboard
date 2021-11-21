from flask import make_response

def create_response(message='',status_code=200, mimetype='application/json'):
        print(message)
        response = make_response(message)
        print(response)
        response.status_code = status_code
        response.mimetype = mimetype
        return response