from z3 import *
import data_structures as DS
import re

class Z3_Worker():
    # def __init__(self):
    #     print('working')

    # split code line by line
    def code_to_list(self, code):
        return code.split(',')

    # create PEMDAS tree
    # def expression_splitter(self, expression):
    #     tree = DS.OperationsTree(expression)
    #     return tree.show_children(tree.node)

    # is this a definition
    def is_definition(self, code):
        return '=' in code

    # solve the proof
    def algebraic_solver(self, expressions):
        x = Real('x')
        s = Solver()
        
        master_expression = ""
        for index, expression in enumerate(expressions):
            s.add(x==eval(expression))

        return s.check() == sat

    # setup the proof
    def algebraic(self, code):
        # find each line of code
        code_steps = self.code_to_list(code)
        expression_list = []

        # clean each line of code to an expression
        for expression in code_steps:
            if self.is_definition(expression):
                expression = expression.split('=')[1]
                expression_list.append(expression)

        # handle expressions and proof
        return self.algebraic_solver(expression_list)

    def inequality(self, code):
        print('clalled')

if __name__ == '__main__':
    import json
    test = Z3_Worker()
    print(test.algebraic(json.loads('{"type": "algebraic", "code": "x=2*3+4-2,x=6+4-4,x=10-2,x=8"}')['code']))