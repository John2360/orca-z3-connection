from z3 import *
import data_structures as DS
import re

class Z3_Worker():
    def info_on_expression(self, expression):
        regex = r'\b[^\d\W]+\b'
        varibles = re.findall(regex, expression)

        varibles = set(varibles)

        return varibles

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
    
    #returns true if string contains a letter (caps or no caps)
    def has_letters(self, string):
        letters = [chr(i) for i in range (65,91)]
        letters.extend([chr(i) for i in range(97, 123)])
        for letter in letters:
            if letter in string:
                return True
        
        return False
    
    #returns True if there is no operator and there is a letter variable on the left
    #of the inequality. No inequality returns False
    def is_bounding(self, expression):
        if '>' in expression:
            index = expression.index('>')
        elif '<' in expression:
            index = expression.index('<')
        else:
            return False

        for op in ['+', '-', '/', '*']:
            if op in expression[0:index]:
                return False
        
        if self.has_letters(expression[0:index]):
            return True
        else:
            return False
    
    #returns a tuple of ([free vars], [bound vars])
    def separate_vars(self, expressions):
        vars = set()
        bound = set()
        for expression in expressions:
            for var in self.info_on_expression(expression):
                vars.add(var)
                if self.is_bounding(expression):
                    bound.add(var)
        
        vars = list(vars)
        for var in vars:
            if var in bound:
                vars.remove(var)
        
        return (vars, list(bound))
                
        
        
    #returns a tuple of ([free expressions], [bound expressions])
    def separate_expressions(self, expressions):
        free = []
        bound = []

        for expression in expressions:
            if self.is_bounding(expression):
                bound.append(expression)
            else:
                free.append(expression)
        
        return (free, bound)

    # solve the proof
    def algebraic_solver(self, expressions):
        s = Solver()
        
        for expression in expressions:
            varibles = self.info_on_expression(expression)

            for var in varibles:
                exec(var + " = Real('"+var+"')")

            expression = expression.replace('=', '==')
            f = eval(expression)
            s.add(f)

        return (s.check() == sat, None)

    # setup the proof
    def algebraic(self, code):
        # find each line of code
        code_steps = self.code_to_list(code)
        expression_list = []

        # clean each line of code to an expression
        for expression in code_steps:
            if self.is_definition(expression):
                expression_list.append(expression)

        # handle expressions and proof
        return self.algebraic_solver(expression_list)

    def inequality_solver(self, code):
        # find each line of code
        code_steps = self.code_to_list(code)
        expression_list = []

        # clean each line of code to an expression
        for expression in code_steps:
            if self.is_definition(expression):
                expression_list.append(expression)

        s = Solver()

        # keep track of declared varibles to not dupe
        declared_vars = []

        # declare new varibles and add statements to solver
        for expression in expression_list:
            varibles = self.info_on_expression(expression)

            for var in [x for x in varibles if x not in declared_vars]:
                exec(var + " = Real('"+var+"')")

            expression = expression.replace('=', '==')
            f = eval(expression)
            s.add(f)

        if s.check() == sat:
            expression_model = s.model()
        else:
            expression_model = None
        
        return (s.check() == sat, expression_model)

    def inequality(self, code):
        return self.inequality_solver(code)

    def simplify_tool(self, expression):
        varibles = self.info_on_expression(expression)

        for var in varibles:
            exec(var + " = Real('"+var+"')")

        f = eval(expression)
        
        return simplify(f)

if __name__ == '__main__':
    import json
    test = Z3_Worker()
    print(test.algebraic(json.loads('{"type": "algebraic", "code": "x=2*3+4-2,x=6+4-4,x=10-2,x=8"}')['code']))
    print(test.inequality("x=2,y=5,z=x+y,z>3"))
    testExprs = ["x>1","x**2+y**2>1"]
    print("Free:",test.separate_vars(testExprs)[0],"Bound:",test.separate_vars(testExprs)[1])
    print("Free:",test.separate_expressions(testExprs)[0],"Bound:",test.separate_expressions(testExprs)[1])
