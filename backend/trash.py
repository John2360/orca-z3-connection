from z3 import *
from math import sqrt
import re
from itertools import chain, combinations

from sympy import symbols, Eq, solve
import string
from math import sqrt
import copy

import ast

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

class OperationsTree():
    def __init__(self, input):
        self.node = ast.parse(input) 

    def show_children(self, node, level=0):
        if isinstance(node, ast.Num):
            print(' ' * level + str(node.n))
        else:
            print(' ' * level + str(node))
        for child in ast.iter_child_nodes(node):
            self.show_children(child, level+1)

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

    def char_in_str(self, input, list):
        for char in list:
            if char in input:
                return char
        return False
    
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
    
    def format_disjunction(self, expression):
        list = expression.split("or")
        string = "Or("
        for item in list:
            string += item + ","
        return string[0:len(string) - 1] + ")" 
    
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

            if expression.count('=') == 1:
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

            if expression.count('=') == 1:
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
        if modifier != False:
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
                    declared_vars.append(var)
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
        else:
            # keep track of declared varibles to not dupe
            declared_vars = []
            varibles = self.info_on_expression(expression)
            for var in [x for x in varibles if x not in declared_vars]:
                    exec(var + " = Real('"+var+"')")

            return simplify(eval(expression))

    def convert_or_to_z3_or(self, expression):
        if 'or' in expression.lower():
            expression = expression.lower().replace(' or ', ',')
            expression = "["+ expression+"]"
            status = True
        else:
            status = False
        
        return (status, expression)

    def for_all(self, code):
        # find each line of code
        code_steps = self.code_to_list(code)

        s = Solver()

        # keep track of declared varibles to not dupe
        declared_vars = []
        bounding_vars = []

        bounding_expressions = []
        expression_list = []

        # declare new varibles and add statements to solver
        for expression in code_steps:
            old_expression = expression
            or_statement, expression = self.convert_or_to_z3_or(expression)
            varibles = self.info_on_expression(expression)
            
            for var in [x for x in varibles if x not in declared_vars]:
                    declared_vars.append(var)
                    exec(var + " = Real('"+var+"')")

            if self.is_bounding(expression):
                for var in varibles:
                    bounding_vars.append(var)

                bounding_expressions.append(expression)
                
            else:
                expression_list.append(expression)

        exec_expressions = []
        for expression in expression_list:
            clean_vars = []
            varibles = self.info_on_expression(expression)

            for_all_vars = [x for x in varibles if x not in bounding_vars]
            for var in for_all_vars:
                clean_vars.append(locals()[var])
            
            # print(str(expression))
            expression = eval(expression)

            if or_statement:
                exec_expressions.append(ForAll(clean_vars, Or(expression)))
            else:
                exec_expressions.append(ForAll(clean_vars, expression))

        for bounding_expression in bounding_expressions:
            varibles = self.info_on_expression(bounding_expression)
            expression = eval(bounding_expression)
            exec_expressions.append(expression)

        for expression in exec_expressions:
            s.add(expression)
        res = s.check()
        if res == sat:
            expression_model = s.model()
        else:
            if len(set(declared_vars)) > 1 or or_statement:
                return "Counterexample: " + str(self.produce_counterexample(code_steps))
            
            if or_statement:
                differnt_combos = {}
                for index, expression in enumerate(code_steps):
                    or_statement, expression_small = self.convert_or_to_z3_or(expression)
                    if or_statement:
                        split_expression = expression_small.split(',')
                        modified_one = copy.deepcopy(code_steps)
                        modified_one[index] = split_expression[0].replace('[', '').rstrip()
                        differnt_combos[len(differnt_combos)+1] = modified_one
                        
                        modified_two = copy.deepcopy(code_steps)
                        modified_two[index] = split_expression[1].replace(']','').rstrip()
                        differnt_combos[len(differnt_combos)+1] = modified_two

                interval_list = []

                for combo in differnt_combos:
                    new_code_list = ",".join(differnt_combos[combo])
                    bounds, expression = self.find_bounds_input(new_code_list)
                    ints = self.find_bounds(bounds, expression)
                    interval_list.append(self.get_intervals(expression_list, ints))

                return self.simplify_intervals(interval_list)

            else:
                bounds, expression = self.find_bounds_input(code)
                ints = self.find_bounds(bounds, expression)

            return self.get_intervals(expression_list, ints)
        
        return (res == sat, expression_model)
    
    def produce_counterexample(self, expressions):
        s = Solver()
            
        for expression in expressions:
            or_statement, expression = self.convert_or_to_z3_or(expression)
            varibles = self.info_on_expression(expression)

            for var in varibles:
                exec(var + " = Real('"+var+"')")

            if expression.count('=') == 1:
                expression = expression.replace('=', '==')

            f = eval(expression)
            
            if or_statement:
                s.add(Not(Or(f)))
            else:
                s.add(Not(f))
        
        s.check()
        return s.model()

    def break_down_expression(self, expression):
        if '==' in expression:
            return (expression.split('==')[0].strip(),expression.split('==')[1].strip())
        elif '=' in expression:
            return (expression.split('=')[0].strip(),expression.split('=')[1].strip())

    def find_bounds_input(self, expression):
        code_lines = self.code_to_list(expression)

        expression_list = []
        bounds_list = []
        var_list = []
        possible_vars = list(string.ascii_lowercase)
        untaken_vars = [x for x in possible_vars if x not in var_list]
        
        for line in code_lines:
            varibles = self.info_on_expression(line)
            for var in varibles:
                var_list.append(var)

        for index, expression in enumerate(code_lines):
            char = self.char_in_str(expression, ['>', '<', '='])
            if char == '>' or char == '<' or char == '=':
                code_lines[index] = expression.split(char)
                
                for code in code_lines[index]:
                    varibles = self.info_on_expression(code)
        
                    if(len(varibles) > 0):
                        expression_list.append(code)
                    else:
                        bounds_list.append(code)

        for expression in code_lines:
            if expression[0] == expression_list[0]:
                bounds_list.append(expression[1])
            elif expression[1] == expression_list[0]:
                bounds_list.append(expression[0])

        for index, item in enumerate(bounds_list):
            bounds_list[index] = untaken_vars[0] + "=" + item
        
        for index, item in enumerate(expression_list):
            expression_list[index] = untaken_vars[0] + "=" + item

        return (bounds_list, expression_list[0])

    # input bound dict and expression dict
    # bounds = {"y": 4, "y":16} # expression = {"y": "x ** 2"}
    def find_bounds(self, bounds, expression):
        # print(bounds, expression)
        declared_vars = []
        solution_list = []

        # declare varibles
        varibles = self.info_on_expression(expression)
        
        for var in varibles:
            for var in [x for x in varibles if x not in declared_vars]:
                declared_vars.append(var)
                exec(var + " = symbols('"+var+"')")

        # expression
        broke_down = self.break_down_expression(expression)
        master_eq = Eq(eval(broke_down[1]), locals()[broke_down[0]])

        for bound in bounds:
            broke_down = self.break_down_expression(bound)
            bound_eq = Eq(eval(broke_down[1]), locals()[broke_down[0]])
            solution = solve((master_eq, bound_eq), [locals()["x"] for x in declared_vars])
            solution_list.append(solution)

        # just returns xs
        # solution_list = [x[0] for x in solution_list]
        # print(solution_list)

        return solution_list

    def get_intervals(self, ineqs, intersections):
        if type(intersections[0]) is dict:
            return unsat
        points = []
        for list in intersections:
            for point in list:
                points.append(point)

        domainVals = [point[0] for point in points]
        domainVals.sort()
        domainVals.insert(0, domainVals[0] - 1)
        domainVals.append(domainVals[-1] + 1)

        intervals = []

        for i in range(0, len(domainVals) - 1):
            avg = (domainVals[i] + domainVals[i+1])/2
            isInterval = True
            for ineq in ineqs:
                if not self.plug_in(ineq, {"x":avg}):
                    isInterval = False
                    break
            
            if isInterval:
                start = domainVals[i]
                end = domainVals[i+1]
                igrouper = "["
                fgrouper = "]"
                if i + 1 == len(domainVals) - 1:
                    end = "INF"
                    fgrouper = ")"
                if i == 0:
                    start = "-INF"
                    igrouper = "("
                


                for ineq in ineqs:
                    if not self.plug_in(ineq, {"x":domainVals[i]}):
                        igrouper = "("
                        break
                
                for ineq in ineqs:
                    if not self.plug_in(ineq, {"x":domainVals[i+1]}):
                        fgrouper = ")"
                        break 


                intervals.append(igrouper+str(start) + ","+str(end)+fgrouper)

        return self.simplify_intervals(intervals)
        
    def plug_in(self, ineq, valDict):
        string = ineq
        for key in valDict:
            while key in string:
                string = string.replace(key, "("+str(valDict[key])+")")   

        answer = eval(string)
        return answer
    
    def simplify_intervals(self,intervals):
        list = []
        for interval in intervals:
            index = interval.index(',')
            temp = []
            temp.append(interval[0:1])
            try:
                temp.append(self.test_is_int(float(interval[1:index])))
            except:
                temp.append(interval[1:index])
            
            try:
                temp.append(self.test_is_int(float(interval[index + 1: len(interval) - 1])))
            except:
                temp.append(interval[index + 1: len(interval) - 1])

            temp.append(interval[len(interval) - 1:])
            list.append(temp)
        
        bad = []
        i = 0
        while i < len(list):
            if list[i][1] == "-INF":
                bad.append(list[i])
                list.pop(i)
                i -= 1
            i += 1 
        
        list.sort(key=lambda x: x[1])
        for interval in bad:
            list.insert(0, interval)

        i = 0
        while i < len(list) - 1:
            current = list[i]
            next = list[i+1]

            if current == next or current[-2] == "INF" or (next[-2] != "INF" and current[-2] >= next[-2]):
                list.pop(i+1)
                i -= 1
            
            elif next[1] == "-INF":
                list.pop(i)
                i -= 1
            
            elif current[-2] > next[1]:
                list[i][-2] = next[-2]
                list[i][-1] = next[-1]
                list.pop(i+1)
                i -= 1
            
            elif current[-2] == next[1] and (current[-1] == ']' or next[0] == '['):
                list[i][-2] = next[-2]
                list[i][-1] = next[-1]
                list.pop(i+1)
                i -= 1

            i += 1
        for j in range(0,len(list)):
            list[j] = list[j][0] + str(list[j][1]) + ','+str(list[j][2]) + list[j][3]

        return list
    
    def test_is_int(self, val):
        if type(val) is str:
            return val

        if val == int(val):
            return int(val)
        else:
            return val
    
    def get_bounds_powerset(bounds):
        output = list(chain.from_iterable(combinations(bounds,r) for r in range (len(bounds) + 1)))
        output.remove(())
        return output

if __name__ == '__main__':
    import json
    test = Z3_Worker()
    # print(test.algebraic(json.loads('{"type": "algebraic", "code": "x=2*3+4-2,x=6+4-4,x=10-2,x=8"}')['code']))
    # print(test.inequality("x=2,y=5,z=x+y,z>3"))
    # testExprs = ["x>1","x**2+y**2>1"]
    # print("Free:",test.separate_vars(testExprs)[0],"Bound:",test.separate_vars(testExprs)[1])
    # print("Free:",test.separate_expressions(testExprs)[0],"Bound:",test.separate_expressions(testExprs)[1])
    # print(test.for_all('x**2>4,x**2<16'))
    # 
    # bounds, expression = test.find_bounds_input("2 * x > x ** 2 + 4 * x - 1")
    # print(test.get_intervals(["2 * x > x ** 2 + 4 * x - 1"], test.find_bounds(bounds, expression)))

    # bounds, expression = test.find_bounds_input("x > 10, x < 5")
    # print(test.get_intervals(["x > 10", "x < 5"], test.find_bounds(bounds, expression)))

    # print(test.for_all("x**2 + y **2 >=0"))
    # print(test.for_all("x**2>0"))
    # print(test.for_all("x + y > 0"))
    # print(test.convert_or_to_z3_or(x**2 + y**2 > 0))
    print(test.for_all("x == y or y == x"))
    print(test.simplify_intervals(['[-2,0)','(-INF,-2]','(0,INF)','(-INF,-3]']))


    # known axioms
    known_axioms = ["x * var1 ** (var2 - 1) == var1 ** var2"]
    list_of_vars = list(vars)

    for axiom in known_axioms:
        expression_vars = self.get_vars(axiom)

        print(expression_vars)
        if len(expression_vars) <= len(vars):

            for j in range(len(vars)):
                for index, expression_var in enumerate(expression_vars):
                    axiom = axiom.replace(expression_var, list_of_vars[index])

                print(axiom)
                
                # shuffle list
                list_of_vars.append(list_of_vars.pop(0))


    # s.add()