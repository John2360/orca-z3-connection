from z3 import *

class Z3_Worker():
    #returns sat if property is true for all values within the bounds
    #calls get_counterexample, if counter exists, for all is unsat; return unsat and counter
    #if counter exists, return sat
    def for_all(self):
        pass

    #takes statements and negates them
    #returns counterexample if it exists, otherwise sat
    def get_counterexample(self):
        pass