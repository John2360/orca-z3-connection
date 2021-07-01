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
    print(data)

    if 'expressions' in data:
        expression = data['expressions']
    else:
        return json.dumps({"error": "expressions field empty"})
    
    if 'bounds' in data:
        bounds = data['bounds']
    else:
        bounds = ""
    
    if 'types' in data:
        types = data['types']
    else:
        types = ""
    
    results = z3.for_all(expression, bounds, types)

    return json.dumps(results)

@app.route('/simplify', methods=['POST'])
def request_handler_simplify():
    data = json.loads(request.data)
    print(data)

    if 'expression' in data:
        expression = data['expression']
    else:
        return json.dumps({"error": "expression field empty"})

    if 'types' in data:
        types = data['types']
    else:
        types = ""

    results = z3.simplify_tool(expression)

    return json.dumps(results)