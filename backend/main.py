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
    expression = data['expression']
    bounds = data['bounds']
    results = z3.for_all(expression, bounds)

    return json.dumps(results)


# # handles proof checker
# @app.route('/checker', methods=['POST'])
# def request_handler_checker():
#     # proof type
#     data = json.loads(request.data)
#     type = data['type']
    
#     # valid proof types
#     valid_operations = {'algebraic': z3.algebraic, 'inequality': z3.inequality, 'forall': z3.for_all}
#     if type in valid_operations:
#         # if valid proof type executes proof checker
#         json_data = {}
#         try:
#             validity, model, counter_example = valid_operations[type](data['code'])
#             json_data['success'] = True
#             json_data['valid'] = validity
#             json_data['model'] = str(model)
#         except:
#             json_data['success'] = False
#             json_data['valid'] = None
#             json_data['model'] = None
#             json_data['counter_example'] = None
#     else:
#         json_data = {}
#         json_data['success'] = False
#         json_data['valid'] = None
#         json_data['model'] = None
#         json_data['counter_example'] = None
    
#     return json.dumps(json_data)

# # handles proof checker
# @app.route('/simplify', methods=['POST'])
# def request_handler_simplify():
#     try:
#         data = json.loads(request.data)
#         simplified = z3.simplify_tool(data['expression'])
#         json_data = {}
#         json_data['success'] = True
#         json_data['simplified'] = str(simplified)
#     except:
#         json_data = {}
#         json_data['success'] = False
#         json_data['simplified'] = None

#     return json.dumps(json_data)