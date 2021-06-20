#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/orca-z3-connection/backend/")

from main import app as application
application.secret_key = 'testing123'