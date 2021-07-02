from flask import Flask, request
from flask_cors import CORS, cross_origin
from celery import Celery
import z3_methods
import json

import time

# flask setups
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'     # Your celery configurations in a celeryconfig.py

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

z3 = z3_methods.Z3_Worker()

# base page
@app.route('/')
def blank():
    return 'Project Orca Z3 API'

@celery.task
def async_for_all(expression, bounds, types):
    return z3.for_all(expression, bounds, types)

@app.route('/checker', methods=['POST'])
def request_handler_checker():
    data = json.loads(request.data)

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
    
    time.sleep(.25)
    results = async_for_all(expression, bounds, types)

    return json.dumps(results)

@celery.task
def async_simplify_tool(expression):
    return z3.simplify_tool(expression)

@app.route('/simplify', methods=['POST'])
def request_handler_simplify():
    data = json.loads(request.data)

    if 'expression' in data:
        expression = data['expression']
    else:
        return json.dumps({"error": "expression field empty"})

    if 'types' in data:
        types = data['types']
    else:
        types = ""

    time.sleep(.2)
    results = async_simplify_tool(expression)

    return json.dumps(str(results))