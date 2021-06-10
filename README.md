## Project Orca Z3 API ##
Install Z3:
- python script/mk_make.py --prefix=<save to location you can access>
- cd build; make;

Python3 dependencies:
- flask
- z3framework

Run with Python3 in terminal with:
export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:<path to dylib>
export FLASK_APP=main.py
ex: export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/lib/libz3.dylib

Algebraic example 1:
{"type": "algebraic, "code": "x=2*3+4,x=6+4,x=10"}