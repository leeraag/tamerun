from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app, template = {
    "swagger": "2.0",
    "info": {
        'title': 'API for tamerun-invest',
        'version': '1.0',
        'description': 'API for calculating the forecast of real estate '
                       'banking transactions'
    }
})

"""
Convert to json result
:param key: key for json
:param result: result calculations
:param code: result code
:return: result calculations in json format
"""
def to_result_json(key, result, code):
    return jsonify({
        key: result
    }), code

@app.route('/api/<int:first>/<int:second>', methods=['GET'])
def calculation(first, second):
    return to_result_json('result', first + second, 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0')