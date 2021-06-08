from z3 import *
import data_structures as DS
import re

class Z3_Worker():
    def info_on_expression(self, expression):
        regex = r'\b[^\d\W]+\b'
        varibles = re.findall(regex, expression)

        varibles = set(varibles)

        return varibles

    def char_in_str(self, input, list):
        for char in list:
            if char in input:
                return char

        return False

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

        s = Solver()

        # keep track of declared varibles to not dupe
        declared_vars = []

        # declare new varibles and add statements to solver
        for expression in code_steps:
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
        expression_list = []

        modifier = self.char_in_str(expression, ['>', '<', '='])
        final_modifier = ''

        if modifier in ['>', '<', '=']:
            if self.char_in_str(expression, ['=']):
                final_modifier = modifier + '='
                expression_list = expression.split(modifier+'=')
            else:
                final_modifier = modifier
                expression_list = expression.split(modifier)

        # hold simplified expression
        simplified_expressions = []

        # keep track of declared varibles to not dupe
        declared_vars = []

        # declare new varibles and add statements to solver
        # simplify each side and add it to a list
        for index, expression in enumerate(expression_list):
            varibles = self.info_on_expression(expression)
            
            for var in [x for x in varibles if x not in declared_vars]:
                exec(var + " = Real('"+var+"')")

            f = eval(expression)
            if type(f) == z3.z3.ArithRef:
                simplified = simplify(f)
            else:
                simplified = f
            
            if type(simplified) == z3.z3.BoolRef:
                if simplified or not simplified:
                    simplified_expressions.append(expression_list[index])
            else:
                simplified_expressions.append(simplified)

        # simplify the combined statements
        combined_expression = eval(final_modifier.join([str(elem) for elem in simplified_expressions]))
        if combined_expression == True:
            return final_modifier.join([str(elem) for elem in simplified_expressions])

        final_expression = simplify(combined_expression)

        if str(final_expression) == 'True' or str(final_expression) == 'False':
            if final_expression or not final_expression:
                return str(combined_expression)
        else:
            return final_expression

if __name__ == '__main__':
    import json
    test = Z3_Worker()
    # print(test.algebraic(json.loads('{"type": "algebraic", "code": "x=2*3+4-2,x=6+4-4,x=10-2,x=8"}')['code']))
    # print(test.simplify_tool("7*x**2-4*x**2 == 0"))
    print(test.inequality("x>3, z=x, z>4"))