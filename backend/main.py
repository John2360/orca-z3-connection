from flask import Flask, request
import z3_methods
import json

# flask setups
app = Flask(__name__)
z3 = z3_methods.Z3_Worker()

# base page
@app.route('/')
def blank():
    return 'Project Orca Z3 API'

# handles proof checker
@app.route('/checker', methods=['POST'])
def request_handler():
    # proof type
    data = json.loads(request.data)
    type = data['type']
    
    # valid proof types
    valid_operations = {'algebraic': z3.algebraic, 'inequality': z3.inequality}
    if type in valid_operations:
        # if valid proof type executes proof checker
        json_data = {}
        validity, model = valid_operations[type](data['code'])
        json_data['success'] = True
        json_data['valid'] = validity
        json_data['model'] = str(model)
        return json.dumps(json_data)
    else:
        json_data = {}
        json_data['success'] = False
        json_data['valid'] = None
        json_data['model'] = None
        return json.dumps(json_data)