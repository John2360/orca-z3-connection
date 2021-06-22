from z3 import *
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
    
    def simplify_tool(self, expression, types=''):
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

            return {'simplified': simplify(eval(expression))}

    def convert_or_to_z3_or(self, expression):
            if 'or' in expression.lower():
                expression = expression.lower().replace(' or ', ',')
                expression = "["+ expression+"]"
                status = True
            else:
                status = False
            
            return (status, expression)

    # returns sat if property is true for all values within the bounds
    # calls get_counterexample, if counter exists, for all is unsat; return unsat and counter
    # if counter exists, return sat
    def for_all(self, expressions, bounds="", types=""):
        expressionList = expressions.split(',')
        typeDict = self.generate_type_dict(types)
        if bounds == "":
            boundList = []
        else:
            boundList = bounds.split(',')
        counter_example = self.get_counterexample(expressionList, boundList,typeDict)

        if counter_example == "BAD_BOUNDS":
            return {'status':'unsat', 'counter':'BAD_BOUNDS'}
        elif counter_example['status'] == sat:
            return {'status':"unsat", 'counter': str(counter_example['counter'])}

        elif counter_example['status'] == unsat:
            return {"status": "sat"}
    
    def get_vars(self, expressions):
        vars = set()
        for expression in expressions:
            for var in self.info_on_expression(expression):
                if var != "or":
                    vars.add(var)
        
        return vars
    
    def init_var(self, var, type):
        return var + "=" + type +"('" + var + "')"
    
    def generate_type_dict(self, assignments):
        types = {}
        temp = assignments.replace(' ', '')
        list = assignments.split(',')
        for assignment in list:
            if '(' in assignment and ')' in assignment:
                i = assignment.index('(')
                j = assignment.index(')')
                type = assignment[0:i]
                var = assignment[i+1:j]
                if type in types:
                    types[type].append(var)
                else:
                    types[type] = [var]
        
        return types


    # Not(p,q,r) == Not(p) or Not(q) or Not(r)
    def de_morgans(self, expressions):
        str = "Or("
        for expression in expressions:
            str += "Not("+expression +"),"
        
        return str[0:len(str) - 1] + ")"
        
    # takes statements and negates them
    # returns counterexample if it exists, otherwise sat
    def get_counterexample(self, expressions, bounds=[], types={}):
        vars = self.get_vars(expressions)

        if len(bounds) > 0:
            vars.update(self.get_vars(bounds))
        
        s = Solver()
        declared = []
        for type in types:
            for var in vars:
                if var in types[type]:
                    declared.append(var)
                    executable = self.init_var(var, type)
                    exec(executable)
        
        for var in vars:
            if var not in declared:
                executable = self.init_var(var, "Real")
                exec(executable)
        
        for i in range(len(expressions)):
            if ' or ' in expressions[i]:
                expressions[i] = 'Or(' + self.convert_or_to_z3_or(expressions[i])[1] + ')'
        
        for i in range(len(bounds)):
            if ' or ' in bounds[i]:
                bounds[i] = 'Or(' + self.convert_or_to_z3_or(bounds[i])[1] + ')'
        
        for bound in bounds:
            s.add(eval(bound))

        if s.check() == unsat:
            return "BAD_BOUNDS"

        s.add(eval(self.de_morgans(expressions)))

        
        res = s.check()
        model = None
        if res == sat:
            model = s.model()
        
        return {"status":res, "counter":model}

if __name__ == '__main__':
    test = Z3_Worker()
    print(test.de_morgans(["x**2>2","x**2<-2"]))
    print(test.for_all("x**2>16","x>4 or x<-4"))
    print(test.for_all("x+y>0"))
    print(test.for_all("x**2>=0","x>2,x<2"))
    print(test.for_all('y>1,y-1>0,y>y-1','y>0,y!=1','Int(y)'))
