# Replace with your own path
# export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/lib/libz3.dylib

from z3 import *

x = Real('x')
y = Real('y')
s = Solver()
s.add(x + y > 5, x > 1, y > 1)
print(s.check())
print(s.model())