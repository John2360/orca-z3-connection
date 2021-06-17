from flask import Flask, request
from flask_cors import CORS, cross_origin
import z3_methods
import json

# flask setups
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

z3 = z3_methods.Z3_Worker()

# base page
@app.route('/')
def blank():
    return 'Project Orca Z3 API'


@app.route('/checker', methods=['POST'])
def request_handler_checker():
    data = json.loads(request.data)
    expression = data['expressions']
    bounds = data['bounds']
    results = z3.for_all(expression, bounds)

    return json.dumps(results)