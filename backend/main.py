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
        return json.dump('{"success": "true", "valid: "'+str(valid_operations[type](data['code']))+'}')
    else:
        return json.dump('{"success": "false", "valid: "invalid"}')