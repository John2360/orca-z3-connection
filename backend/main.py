from flask import Flask, request
import z3_methods
import json

app = Flask(__name__)
z3 = z3_methods.Z3_Worker()

@app.route('/')
def blank():
    return 'Project Orca Z3 API'

@app.route('/solver', methods=['POST'])
def request_handler():
    data = json.loads(request.data)
    type = data['type']
    
    valid_operations = {'algebraic': z3.algebraic, 'inequality': z3.inequality}
    if type in valid_operations:
        return '{"valid: "'+str(valid_operations[type](data['code']))+'}'
    else:
        return 'Error: Type not found.'